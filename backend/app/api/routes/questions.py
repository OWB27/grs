from fastapi import APIRouter, Query

from app.services.question_service import get_questions

router = APIRouter()


@router.get("/questions")
def fetch_questions(lang: str = Query(default="zh")) -> dict:
    # 当前阶段保留 lang 参数，但先统一返回双语结构，
    # 以适配你当前前端统一后的 shape。
    return {"questions": get_questions()}