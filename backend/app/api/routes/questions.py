from fastapi import APIRouter, Query

from app.services.question_service import get_questions_by_lang

router = APIRouter()


@router.get("/questions")
def get_questions(lang: str = Query(default="zh")) -> dict:
    return {"questions": get_questions_by_lang(lang)}