from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.questions import QuestionsResponse
from app.services.question_service import get_questions

router = APIRouter()


@router.get("/questions", response_model=QuestionsResponse)
def fetch_questions(
    session: Session = Depends(get_session),
) -> QuestionsResponse:
    return QuestionsResponse(questions=get_questions(session))