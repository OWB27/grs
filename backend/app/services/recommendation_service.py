from sqlmodel import Session, select

from app.db.models import Game, GameTag, Tag
from app.schemas.recommend import RecommendResponse


from sqlmodel import Session, select

from app.db.models import Game, GameTag, Tag


def score_games(session: Session, user_profile: dict[str, int]) -> list[dict]:
    positive_profile = {
        tag_code: score
        for tag_code, score in user_profile.items()
        if score > 0
    }

    if not positive_profile:
        return []

    statement = (
        select(Game, GameTag, Tag)
        .join(GameTag, GameTag.game_id == Game.id)
        .join(Tag, Tag.id == GameTag.tag_id)
        .where(Game.is_active == True)  # noqa: E712
        .where(Tag.code.in_(list(positive_profile.keys())))
    )

    rows = session.exec(statement).all()

    scored_by_game_id: dict[int, dict] = {}

    for game, game_tag, tag in rows:
        user_weight = positive_profile.get(tag.code, 0)
        if user_weight <= 0:
            continue

        contribution = user_weight * game_tag.weight

        existing = scored_by_game_id.get(game.id)
        if not existing:
            existing = {
                "game": game,
                "score": 0,
                "matchedTags": [],
            }
            scored_by_game_id[game.id] = existing

        existing["score"] += contribution
        existing["matchedTags"].append(
            {
                "tagCode": tag.code,
                "tagNameZh": tag.name_zh,
                "tagNameEn": tag.name_en,
                "gameWeight": game_tag.weight,
                "userWeight": user_weight,
                "contribution": contribution,
            }
        )

    scored_candidates = list(scored_by_game_id.values())

    for candidate in scored_candidates:
        candidate["matchedTags"].sort(
            key=lambda item: item["contribution"],
            reverse=True,
        )

    scored_candidates.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored_candidates


def select_top_candidates(scored_candidates: list[dict], limit: int = 9) -> list[dict]:
    if limit <= 0:
        return []

    positive_candidates = [
        item for item in scored_candidates if item["score"] > 0
    ]

    return positive_candidates[:limit]


def build_recommend_response(reasoned_candidates: list[dict]) -> RecommendResponse:
    recommendations = []

    for candidate in reasoned_candidates:
        game = candidate["game"]

        recommendations.append(
            {
                "gameId": game.id,
                "name": {
                    "zh": game.name_zh,
                    "en": game.name_en,
                },
                "steamUrl": game.steam_url,
                "coverImageUrl": game.cover_image_url,
                "reason": candidate["reason"],
                "debug": {
                    "score": candidate["score"],
                    "rankingMode": candidate.get("rankingMode", "rule_based"),
                    "matchedTags": [
                        {
                            "tagCode": item["tagCode"],
                            "tagNameZh": item["tagNameZh"],
                            "tagNameEn": item["tagNameEn"],
                            "gameWeight": item["gameWeight"],
                            "userWeight": item["userWeight"],
                            "contribution": item["contribution"],
                        }
                        for item in candidate["matchedTags"]
                    ],
                },
            }
        )

    return RecommendResponse(recommendations=recommendations)