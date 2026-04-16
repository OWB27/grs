from fastapi import APIRouter, Query, HTTPException

from app.schemas.questions import QuestionsResponse
from app.schemas.common import ErrorResponse
from app.services.question_service import get_questions

router = APIRouter()


@router.get(
    "/questions",
    response_model=QuestionsResponse,
    responses={
        400: {"model": ErrorResponse},
    },
)
def fetch_questions(lang: str = Query(default="zh")) -> QuestionsResponse:
    if lang not in {"zh", "en"}:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "INVALID_LANG",
                    "message": "lang must be 'zh' or 'en'.",
                }
            },
        )

    return QuestionsResponse(questions=get_questions())