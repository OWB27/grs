from sqlmodel import Session, select

from app.db.models import Question, QuestionOption


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


def get_questions(session: Session) -> list[dict]:
    questions = session.exec(
        select(Question).order_by(Question.sort_order)
    ).all()

    result = []

    for question in questions:
        options = session.exec(
            select(QuestionOption).where(QuestionOption.question_id == question.id)
        ).all()

        result.append(serialize_question(question, options))

    return result