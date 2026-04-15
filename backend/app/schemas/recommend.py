from pydantic import BaseModel


class AnswerItem(BaseModel):
    question_id: int
    option_id: int


class RecommendationItem(BaseModel):
    game_id: int
    name_zh: str | None = None
    name_en: str
    steam_url: str
    reason: str


class RecommendRequest(BaseModel):
    answers: list[AnswerItem]
    lang: str = "zh"


class RecommendResponse(BaseModel):
    recommendations: list[RecommendationItem]