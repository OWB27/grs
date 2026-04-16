from pydantic import BaseModel

from app.schemas.common import LocalizedText


class AnswerItem(BaseModel):
    questionId: int
    optionId: int


class DebugTagItem(BaseModel):
    tagCode: str
    weight: int


class DebugInfo(BaseModel):
    score: float
    rankingMode: str
    matchedTags: list[DebugTagItem]


class RecommendationItem(BaseModel):
    gameId: int
    name: LocalizedText
    steamUrl: str
    reason: LocalizedText
    debug: DebugInfo | None = None


class RecommendRequest(BaseModel):
    answers: list[AnswerItem]


class RecommendResponse(BaseModel):
    recommendations: list[RecommendationItem]
