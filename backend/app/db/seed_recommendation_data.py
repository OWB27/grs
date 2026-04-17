from sqlmodel import Session, select

from app.db.engine import engine
from app.db.models import (
    Game,
    GameTag,
    OptionTagWeight,
    QuestionOption,
    Tag,
)


TAG_SEEDS = [
    {"code": "story_rich", "name_zh": "剧情沉浸", "name_en": "Story Rich"},
    {"code": "character_growth", "name_zh": "角色成长", "name_en": "Character Growth"},
    {"code": "open_world", "name_zh": "开放世界", "name_en": "Open World"},
    {"code": "exploration", "name_zh": "探索", "name_en": "Exploration"},
    {"code": "fast_paced", "name_zh": "快节奏", "name_en": "Fast Paced"},
    {"code": "combat", "name_zh": "战斗", "name_en": "Combat"},
    {"code": "challenge", "name_zh": "挑战", "name_en": "Challenge"},
    {"code": "competitive", "name_zh": "竞技", "name_en": "Competitive"},
    {"code": "relaxed", "name_zh": "轻松", "name_en": "Relaxed"},
]

GAME_SEEDS = [
    {
        "code": "witcher_3",
        "name_zh": "巫师 3：狂猎",
        "name_en": "The Witcher 3: Wild Hunt",
        "steam_url": "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/",
        "cover_image_url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/292030/header.jpg",
    },
    {
        "code": "disco_elysium",
        "name_zh": "极乐迪斯科",
        "name_en": "Disco Elysium",
        "steam_url": "https://store.steampowered.com/app/632470/Disco_Elysium__The_Final_Cut/",
        "cover_image_url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/632470/header.jpg",
    },
    {
        "code": "cyberpunk_2077",
        "name_zh": "赛博朋克 2077",
        "name_en": "Cyberpunk 2077",
        "steam_url": "https://store.steampowered.com/app/1091500/Cyberpunk_2077/",
        "cover_image_url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/header.jpg",
    },
    {
        "code": "hades",
        "name_zh": "黑帝斯",
        "name_en": "Hades",
        "steam_url": "https://store.steampowered.com/app/1145360/Hades/",
        "cover_image_url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1145360/header.jpg",
    },
    {
        "code": "monster_hunter_world",
        "name_zh": "怪物猎人：世界",
        "name_en": "Monster Hunter: World",
        "steam_url": "https://store.steampowered.com/app/582010/Monster_Hunter_World/",
        "cover_image_url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/582010/header.jpg",
    },
    {
        "code": "apex_legends",
        "name_zh": "Apex Legends",
        "name_en": "Apex Legends",
        "steam_url": "https://store.steampowered.com/app/1172470/Apex_Legends/",
        "cover_image_url": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1172470/header.jpg",
    },
]

GAME_TAG_SEEDS = {
    "witcher_3": {
        "story_rich": 5,
        "character_growth": 4,
        "open_world": 4,
        "exploration": 3,
    },
    "disco_elysium": {
        "story_rich": 5,
        "character_growth": 5,
        "relaxed": 2,
    },
    "cyberpunk_2077": {
        "story_rich": 4,
        "open_world": 4,
        "exploration": 3,
        "combat": 2,
    },
    "hades": {
        "fast_paced": 5,
        "combat": 5,
        "challenge": 4,
    },
    "monster_hunter_world": {
        "combat": 4,
        "challenge": 4,
        "exploration": 2,
    },
    "apex_legends": {
        "fast_paced": 5,
        "competitive": 5,
        "combat": 4,
    },
}

OPTION_TAG_WEIGHT_SEEDS = {
    # question 1
    "story_immersion": {
        "story_rich": 5,
        "character_growth": 3,
        "open_world": 2,
    },
    "free_exploration": {
        "open_world": 5,
        "exploration": 4,
        "relaxed": 1,
    },
    "competitive_challenge": {
        "competitive": 5,
        "challenge": 4,
        "combat": 3,
    },
    # question 2
    "slow_relaxed": {
        "relaxed": 5,
        "story_rich": 2,
        "exploration": 2,
    },
    "balanced_pace": {
        "story_rich": 2,
        "combat": 2,
        "exploration": 2,
    },
    "fast_intense": {
        "fast_paced": 5,
        "combat": 4,
        "challenge": 3,
    },
}


def seed_tags(session: Session) -> dict[str, Tag]:
    existing_tags = session.exec(select(Tag)).all()
    if existing_tags:
        return {tag.code: tag for tag in existing_tags}

    for item in TAG_SEEDS:
        session.add(
            Tag(
                code=item["code"],
                name_zh=item["name_zh"],
                name_en=item["name_en"],
                is_active=True,
            )
        )

    session.commit()
    tags = session.exec(select(Tag)).all()
    return {tag.code: tag for tag in tags}


def seed_games(session: Session) -> dict[str, Game]:
    existing_games = session.exec(select(Game)).all()
    if existing_games:
        return {game.code: game for game in existing_games}

    for item in GAME_SEEDS:
        session.add(
            Game(
                code=item["code"],
                name_zh=item["name_zh"],
                name_en=item["name_en"],
                steam_url=item["steam_url"],
                cover_image_url=item["cover_image_url"],
                is_active=True,
            )
        )

    session.commit()
    games = session.exec(select(Game)).all()
    return {game.code: game for game in games}


def seed_game_tags(session: Session, games_by_code: dict[str, Game], tags_by_code: dict[str, Tag]) -> None:
    existing = session.exec(select(GameTag)).first()
    if existing:
        return

    for game_code, tag_weights in GAME_TAG_SEEDS.items():
        game = games_by_code[game_code]

        for tag_code, weight in tag_weights.items():
            tag = tags_by_code[tag_code]
            session.add(
                GameTag(
                    game_id=game.id,
                    tag_id=tag.id,
                    weight=weight,
                )
            )

    session.commit()


def seed_option_tag_weights(session: Session, tags_by_code: dict[str, Tag]) -> None:
    existing = session.exec(select(OptionTagWeight)).first()
    if existing:
        return

    options = session.exec(select(QuestionOption)).all()
    options_by_code = {option.code: option for option in options}

    for option_code, tag_weights in OPTION_TAG_WEIGHT_SEEDS.items():
        option = options_by_code.get(option_code)
        if not option:
            raise RuntimeError(
                f"QuestionOption with code '{option_code}' was not found. "
                "Make sure questions/options seed has already run."
            )

        for tag_code, weight in tag_weights.items():
            tag = tags_by_code[tag_code]
            session.add(
                OptionTagWeight(
                    option_id=option.id,
                    tag_id=tag.id,
                    weight=weight,
                )
            )

    session.commit()


def seed_recommendation_data() -> None:
    with Session(engine) as session:
        tags_by_code = seed_tags(session)
        games_by_code = seed_games(session)
        seed_game_tags(session, games_by_code, tags_by_code)
        seed_option_tag_weights(session, tags_by_code)

    print("Recommendation data seeded.")


if __name__ == "__main__":
    seed_recommendation_data()