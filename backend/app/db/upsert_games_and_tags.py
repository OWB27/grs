import json
from pathlib import Path

from sqlmodel import Session, select

from app.db.engine import engine
from app.db.models import Game, GameTag, Tag


BASE_DIR = Path(__file__).resolve().parents[2]
SEEDS_DIR = BASE_DIR / "data_pipeline" / "seeds"

GAMES_FILE = SEEDS_DIR / "games_final.json"
GAME_TAGS_FILE = SEEDS_DIR / "game_tags_final.json"


def load_json(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Seed file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def upsert_games(session: Session) -> dict[str, Game]:
    items = load_json(GAMES_FILE)

    existing_games = session.exec(select(Game)).all()
    games_by_code = {game.code: game for game in existing_games}

    for item in items:
        existing_game = games_by_code.get(item["code"])

        if existing_game:
            existing_game.steam_app_id = item.get("steam_app_id")
            existing_game.steam_url = item["steam_url"]
            existing_game.name_zh = item["name_zh"]
            existing_game.name_en = item["name_en"]
            existing_game.cover_image_url = item.get("cover_image_url")
            existing_game.is_active = item.get("is_active", True)
            session.add(existing_game)
        else:
            new_game = Game(
                code=item["code"],
                steam_app_id=item.get("steam_app_id"),
                steam_url=item["steam_url"],
                name_zh=item["name_zh"],
                name_en=item["name_en"],
                cover_image_url=item.get("cover_image_url"),
                is_active=item.get("is_active", True),
            )
            session.add(new_game)

    session.commit()

    all_games = session.exec(select(Game)).all()
    return {game.code: game for game in all_games}


def upsert_game_tags(session: Session, games_by_code: dict[str, Game]) -> None:
    items = load_json(GAME_TAGS_FILE)

    all_tags = session.exec(select(Tag)).all()
    tags_by_code = {tag.code: tag for tag in all_tags}

    existing_game_tags = session.exec(select(GameTag)).all()
    game_tags_by_pair = {
        (game_tag.game_id, game_tag.tag_id): game_tag
        for game_tag in existing_game_tags
    }

    for item in items:
        game = games_by_code.get(item["game_code"])
        if not game:
            raise RuntimeError(
                f"Game with code '{item['game_code']}' was not found while upserting game_tags."
            )

        tag = tags_by_code.get(item["tag_code"])
        if not tag:
            raise RuntimeError(
                f"Tag with code '{item['tag_code']}' was not found while upserting game_tags."
            )

        pair_key = (game.id, tag.id)
        existing_game_tag = game_tags_by_pair.get(pair_key)

        if existing_game_tag:
            existing_game_tag.weight = item["weight"]
            session.add(existing_game_tag)
        else:
            new_game_tag = GameTag(
                game_id=game.id,
                tag_id=tag.id,
                weight=item["weight"],
            )
            session.add(new_game_tag)

    session.commit()


def upsert_games_and_tags() -> None:
    with Session(engine) as session:
        games_by_code = upsert_games(session)
        upsert_game_tags(session, games_by_code)

    print("Games and game_tags upsert completed.")


if __name__ == "__main__":
    upsert_games_and_tags() 