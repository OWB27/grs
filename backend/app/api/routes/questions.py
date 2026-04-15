from fastapi import APIRouter

from app.services.question_service import get_questions

router = APIRouter()


@router.get("/questions")
def fetch_questions() -> dict:
    return {"questions": get_questions()}
