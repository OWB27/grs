from sqlmodel import Session, select

from app.db.models import OptionTagWeight, Tag
from app.schemas.recommend import AnswerItem


def build_user_profile(session: Session, validated_answers: list[AnswerItem]) -> dict[str, int]:
    user_profile: dict[str, int] = {}

    for answer in validated_answers:
        statement = (
            select(OptionTagWeight, Tag)
            .join(Tag, Tag.id == OptionTagWeight.tag_id)
            .where(OptionTagWeight.option_id == answer.optionId)
        )

        rows = session.exec(statement).all()

        for option_tag_weight, tag in rows:
            current_score = user_profile.get(tag.code, 0)
            user_profile[tag.code] = current_score + option_tag_weight.weight

    return user_profile