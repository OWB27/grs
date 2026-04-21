from sqlmodel import Session, select

from app.db.models import Game, GameTag, Tag
from app.schemas.recommend import RecommendResponse


def score_games(session: Session, user_profile: dict[str, int]) -> list[dict]:
    games = session.exec(
        select(Game).where(Game.is_active == True)  # noqa: E712
    ).all()

    scored_candidates: list[dict] = []

    for game in games:
        statement = (
            select(GameTag, Tag)
            .join(Tag, Tag.id == GameTag.tag_id)
            .where(GameTag.game_id == game.id)
        )
        rows = session.exec(statement).all()

        total_score = 0
        matched_tags: list[dict] = []

        for game_tag, tag in rows:
            user_weight = user_profile.get(tag.code, 0)

            if user_weight <= 0:
                continue

            contribution = user_weight * game_tag.weight
            total_score += contribution

            matched_tags.append(
                {
                    "tagCode": tag.code,
                    "tagNameZh": tag.name_zh,
                    "tagNameEn": tag.name_en,
                    "gameWeight": game_tag.weight,
                    "userWeight": user_weight,
                    "contribution": contribution,
                }
            )

        scored_candidates.append(
            {
                "game": game,
                "score": total_score,
                "matchedTags": sorted(
                    matched_tags,
                    key=lambda item: item["contribution"],
                    reverse=True,
                ),
            }
        )

    scored_candidates.sort(key=lambda item: item["score"], reverse=True)
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