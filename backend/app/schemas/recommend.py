from pydantic import BaseModel


class AnswerItem(BaseModel):
    questionId: int
    optionId: int


class LocalizedText(BaseModel):
    zh: str
    en: str


class RecommendationItem(BaseModel):
    gameId: int
    name: LocalizedText
    steamUrl: str
    reason: LocalizedText


class RecommendRequest(BaseModel):
    answers: list[AnswerItem]
    lang: str = "zh"


class RecommendResponse(BaseModel):
    recommendations: list[RecommendationItem]