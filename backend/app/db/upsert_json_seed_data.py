import json
from pathlib import Path

from sqlmodel import Session, select

from app.db.engine import engine
from app.db.models import (
    Game,
    GameTag,
    OptionTagWeight,
    Question,
    QuestionOption,
    Tag,
)


BASE_DIR = Path(__file__).resolve().parents[2]
SEEDS_DIR = BASE_DIR / "data_pipeline" / "seeds"

TAGS_FILE = SEEDS_DIR / "tags.json"
GAMES_FILE = SEEDS_DIR / "games_final.json"
GAME_TAGS_FILE = SEEDS_DIR / "game_tags_final.json"
QUESTIONS_FILE = SEEDS_DIR / "questions_final.json"
OPTION_TAG_WEIGHTS_FILE = SEEDS_DIR / "option_tag_weights_final.json"


def load_json(file_path: Path):
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(value):
    if isinstance(value, str):
        return value.strip()
    return value


def upsert_tags(session: Session) -> dict[str, Tag]:
    items = load_json(TAGS_FILE)

    existing_tags = session.exec(select(Tag)).all()
    existing_tags_by_code = {tag.code: tag for tag in existing_tags}

    for item in items:
        code = normalize_text(item["code"])
        name_zh = normalize_text(item["name_zh"])
        name_en = normalize_text(item["name_en"])
        is_active = item.get("is_active", True)

        existing_tag = existing_tags_by_code.get(code)

        if existing_tag:
            existing_tag.name_zh = name_zh
            existing_tag.name_en = name_en
            existing_tag.is_active = is_active
        else:
            new_tag = Tag(
                code=code,
                name_zh=name_zh,
                name_en=name_en,
                is_active=is_active,
            )
            session.add(new_tag)
            existing_tags_by_code[code] = new_tag

    session.commit()

    tags = session.exec(select(Tag)).all()
    return {tag.code: tag for tag in tags}


def upsert_games(session: Session) -> dict[str, Game]:
    items = load_json(GAMES_FILE)

    existing_games = session.exec(select(Game)).all()
    existing_games_by_code = {game.code: game for game in existing_games}

    for item in items:
        code = normalize_text(item["code"])
        name_zh = normalize_text(item["name_zh"])
        name_en = normalize_text(item["name_en"])
        steam_url = normalize_text(item["steam_url"])
        cover_image_url = normalize_text(item.get("cover_image_url"))
        is_active = item.get("is_active", True)

        existing_game = existing_games_by_code.get(code)

        if existing_game:
            existing_game.name_zh = name_zh
            existing_game.name_en = name_en
            existing_game.steam_url = steam_url
            existing_game.cover_image_url = cover_image_url
            existing_game.is_active = is_active
        else:
            new_game = Game(
                code=code,
                name_zh=name_zh,
                name_en=name_en,
                steam_url=steam_url,
                cover_image_url=cover_image_url,
                is_active=is_active,
            )
            session.add(new_game)
            existing_games_by_code[code] = new_game

    session.commit()

    games = session.exec(select(Game)).all()
    return {game.code: game for game in games}


def upsert_game_tags(
    session: Session,
    games_by_code: dict[str, Game],
    tags_by_code: dict[str, Tag],
) -> None:
    items = load_json(GAME_TAGS_FILE)

    existing_game_tags = session.exec(select(GameTag)).all()
    existing_game_tags_by_pair = {
        (game_tag.game_id, game_tag.tag_id): game_tag
        for game_tag in existing_game_tags
    }

    for item in items:
        game_code = normalize_text(item["game_code"])
        tag_code = normalize_text(item["tag_code"])
        weight = item["weight"]

        game = games_by_code.get(game_code)
        if not game:
            raise RuntimeError(
                f"Game with code '{game_code}' was not found while importing game_tags."
            )

        tag = tags_by_code.get(tag_code)
        if not tag:
            raise RuntimeError(
                f"Tag with code '{tag_code}' was not found while importing game_tags."
            )

        key = (game.id, tag.id)
        existing_game_tag = existing_game_tags_by_pair.get(key)

        if existing_game_tag:
            existing_game_tag.weight = weight
        else:
            new_game_tag = GameTag(
                game_id=game.id,
                tag_id=tag.id,
                weight=weight,
            )
            session.add(new_game_tag)
            existing_game_tags_by_pair[key] = new_game_tag

    session.commit()


def upsert_questions(session: Session) -> dict[str, QuestionOption]:
    items = load_json(QUESTIONS_FILE)

    existing_questions = session.exec(select(Question)).all()
    existing_questions_by_code = {question.code: question for question in existing_questions}

    existing_options = session.exec(select(QuestionOption)).all()
    existing_options_by_code = {option.code: option for option in existing_options}

    for item in items:
        question_code = normalize_text(item["code"])
        sort_order = item["sort_order"]
        title_zh = normalize_text(item["title_zh"])
        title_en = normalize_text(item["title_en"])

        existing_question = existing_questions_by_code.get(question_code)

        if existing_question:
            existing_question.sort_order = sort_order
            existing_question.title_zh = title_zh
            existing_question.title_en = title_en
            question = existing_question
        else:
            question = Question(
                code=question_code,
                sort_order=sort_order,
                title_zh=title_zh,
                title_en=title_en,
            )
            session.add(question)
            session.flush()
            existing_questions_by_code[question_code] = question

        for option_item in item["options"]:
            option_code = normalize_text(option_item["code"])
            option_sort_order = option_item["sort_order"]
            text_zh = normalize_text(option_item["text_zh"])
            text_en = normalize_text(option_item["text_en"])

            existing_option = existing_options_by_code.get(option_code)

            if existing_option:
                existing_option.question_id = question.id
                existing_option.sort_order = option_sort_order
                existing_option.text_zh = text_zh
                existing_option.text_en = text_en
            else:
                new_option = QuestionOption(
                    question_id=question.id,
                    code=option_code,
                    sort_order=option_sort_order,
                    text_zh=text_zh,
                    text_en=text_en,
                )
                session.add(new_option)
                existing_options_by_code[option_code] = new_option

    session.commit()

    options = session.exec(select(QuestionOption)).all()
    return {option.code: option for option in options}


def upsert_option_tag_weights(
    session: Session,
    options_by_code: dict[str, QuestionOption],
    tags_by_code: dict[str, Tag],
) -> None:
    items = load_json(OPTION_TAG_WEIGHTS_FILE)

    existing_option_tag_weights = session.exec(select(OptionTagWeight)).all()
    existing_option_tag_weights_by_pair = {
        (option_tag_weight.option_id, option_tag_weight.tag_id): option_tag_weight
        for option_tag_weight in existing_option_tag_weights
    }

    for item in items:
        option_code = normalize_text(item["option_code"])
        tag_code = normalize_text(item["tag_code"])
        weight = item["weight"]

        option = options_by_code.get(option_code)
        if not option:
            raise RuntimeError(
                f"QuestionOption with code '{option_code}' was not found while importing option_tag_weights."
            )

        tag = tags_by_code.get(tag_code)
        if not tag:
            raise RuntimeError(
                f"Tag with code '{tag_code}' was not found while importing option_tag_weights."
            )

        key = (option.id, tag.id)
        existing_option_tag_weight = existing_option_tag_weights_by_pair.get(key)

        if existing_option_tag_weight:
            existing_option_tag_weight.weight = weight
        else:
            new_option_tag_weight = OptionTagWeight(
                option_id=option.id,
                tag_id=tag.id,
                weight=weight,
            )
            session.add(new_option_tag_weight)
            existing_option_tag_weights_by_pair[key] = new_option_tag_weight

    session.commit()


def upsert_json_seed_data() -> None:
    with Session(engine) as session:
        tags_by_code = upsert_tags(session)
        games_by_code = upsert_games(session)
        upsert_game_tags(session, games_by_code, tags_by_code)
        options_by_code = upsert_questions(session)
        upsert_option_tag_weights(session, options_by_code, tags_by_code)

    print("JSON seed data upsert completed.")


if __name__ == "__main__":
    upsert_json_seed_data()