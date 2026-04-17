from sqlmodel import Session, select

from app.core.exceptions import AppError
from app.db.models import Question, QuestionOption
from app.schemas.recommend import AnswerItem


def validate_answers(session: Session, answers: list[AnswerItem]) -> list[AnswerItem]:
    if not answers:
        raise AppError(
            code="EMPTY_ANSWERS",
            message="answers must not be empty.",
            status_code=400,
        )

    seen_question_ids: set[int] = set()
    validated_answers: list[AnswerItem] = []

    for answer in answers:
        question = session.get(Question, answer.questionId)
        if not question:
            raise AppError(
                code="QUESTION_NOT_FOUND",
                message=f"questionId {answer.questionId} does not exist.",
                status_code=400,
            )

        option = session.get(QuestionOption, answer.optionId)
        if not option:
            raise AppError(
                code="OPTION_NOT_FOUND",
                message=f"optionId {answer.optionId} does not exist.",
                status_code=400,
            )

        if option.question_id != answer.questionId:
            raise AppError(
                code="OPTION_QUESTION_MISMATCH",
                message=(
                    f"optionId {answer.optionId} does not belong to "
                    f"questionId {answer.questionId}."
                ),
                status_code=400,
            )

        if answer.questionId in seen_question_ids:
            raise AppError(
                code="DUPLICATE_QUESTION_ANSWER",
                message=f"questionId {answer.questionId} is answered more than once.",
                status_code=400,
            )

        seen_question_ids.add(answer.questionId)
        validated_answers.append(answer)

    total_questions = session.exec(select(Question)).all()
    if len(validated_answers) != len(total_questions):
        raise AppError(
            code="INCOMPLETE_ANSWERS",
            message="not all questions have been answered.",
            status_code=400,
        )

    return validated_answers