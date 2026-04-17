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


def import_tags(session: Session) -> dict[str, Tag]:
    items = load_json(TAGS_FILE)

    for item in items:
        session.add(
            Tag(
                code=item["code"],
                name_zh=item["name_zh"],
                name_en=item["name_en"],
                is_active=item.get("is_active", True),
            )
        )

    session.commit()

    tags = session.exec(select(Tag)).all()
    return {tag.code: tag for tag in tags}


def import_games(session: Session) -> dict[str, Game]:
    items = load_json(GAMES_FILE)

    for item in items:
        session.add(
            Game(
                code=item["code"],
                steam_app_id=item.get("steam_app_id"),
                steam_url=item["steam_url"],
                name_zh=item["name_zh"],
                name_en=item["name_en"],
                cover_image_url=item.get("cover_image_url"),
                is_active=item.get("is_active", True),
            )
        )

    session.commit()

    games = session.exec(select(Game)).all()
    return {game.code: game for game in games}


def import_game_tags(
    session: Session,
    games_by_code: dict[str, Game],
    tags_by_code: dict[str, Tag],
) -> None:
    items = load_json(GAME_TAGS_FILE)

    for item in items:
        game = games_by_code.get(item["game_code"])
        if not game:
            raise RuntimeError(
                f"Game with code '{item['game_code']}' was not found while importing game_tags."
            )

        tag = tags_by_code.get(item["tag_code"])
        if not tag:
            raise RuntimeError(
                f"Tag with code '{item['tag_code']}' was not found while importing game_tags."
            )

        session.add(
            GameTag(
                game_id=game.id,
                tag_id=tag.id,
                weight=item["weight"],
            )
        )

    session.commit()


def import_questions(session: Session) -> dict[str, QuestionOption]:
    items = load_json(QUESTIONS_FILE)

    for item in items:
        question = Question(
            code=item["code"],
            sort_order=item["sort_order"],
            title_zh=item["title_zh"],
            title_en=item["title_en"],
        )
        session.add(question)
        session.commit()
        session.refresh(question)

        for option_item in item["options"]:
            session.add(
                QuestionOption(
                    question_id=question.id,
                    code=option_item["code"],
                    sort_order=option_item["sort_order"],
                    text_zh=option_item["text_zh"],
                    text_en=option_item["text_en"],
                )
            )

        session.commit()

    options = session.exec(select(QuestionOption)).all()
    return {option.code: option for option in options}


def import_option_tag_weights(
    session: Session,
    options_by_code: dict[str, QuestionOption],
    tags_by_code: dict[str, Tag],
) -> None:
    items = load_json(OPTION_TAG_WEIGHTS_FILE)

    for item in items:
        option = options_by_code.get(item["option_code"])
        if not option:
            raise RuntimeError(
                f"QuestionOption with code '{item['option_code']}' was not found while importing option_tag_weights."
            )

        tag = tags_by_code.get(item["tag_code"])
        if not tag:
            raise RuntimeError(
                f"Tag with code '{item['tag_code']}' was not found while importing option_tag_weights."
            )

        session.add(
            OptionTagWeight(
                option_id=option.id,
                tag_id=tag.id,
                weight=item["weight"],
            )
        )

    session.commit()


def import_json_seed_data() -> None:
    with Session(engine) as session:
        tags_by_code = import_tags(session)
        games_by_code = import_games(session)
        import_game_tags(session, games_by_code, tags_by_code)
        options_by_code = import_questions(session)
        import_option_tag_weights(session, options_by_code, tags_by_code)

    print("JSON seed data import completed.")


if __name__ == "__main__":
    import_json_seed_data()