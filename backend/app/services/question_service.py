from sqlmodel import Session, select

from app.db.models import Question, QuestionOption


_questions_cache: list[dict] | None = None


def serialize_question(question: Question, options: list[QuestionOption]) -> dict:
    return {
        "id": question.id,
        "code": question.code,
        "sortOrder": question.sort_order,
        "title": {
            "zh": question.title_zh,
            "en": question.title_en,
        },
        "options": [
            {
                "id": option.id,
                "code": option.code,
                "sortOrder": option.sort_order,
                "text": {
                    "zh": option.text_zh,
                    "en": option.text_en,
                },
            }
            for option in sorted(options, key=lambda item: item.sort_order)
        ],
    }


def clear_questions_cache() -> None:
    global _questions_cache
    _questions_cache = None


def build_questions_payload(session: Session) -> list[dict]:
    questions = session.exec(
        select(Question).order_by(Question.sort_order)
    ).all()

    options = session.exec(
        select(QuestionOption).order_by(
            QuestionOption.question_id,
            QuestionOption.sort_order,
        )
    ).all()

    options_by_question_id: dict[int, list[QuestionOption]] = {}
    for option in options:
        options_by_question_id.setdefault(option.question_id, []).append(option)

    return [
        serialize_question(question, options_by_question_id.get(question.id, []))
        for question in questions
    ]


def get_questions(session: Session) -> list[dict]:
    global _questions_cache

    if _questions_cache is not None:
        return _questions_cache

    _questions_cache = build_questions_payload(session)
    return _questions_cache