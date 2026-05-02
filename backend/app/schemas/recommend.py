from pydantic import BaseModel

from app.schemas.common import LocalizedText


class AnswerItem(BaseModel):
    questionId: int
    optionId: int


class DebugTagItem(BaseModel):
    tagCode: str
    tagNameZh: str
    tagNameEn: str
    gameWeight: int
    userWeight: int
    contribution: int


class DebugInfo(BaseModel):
    score: float
    rankingMode: str
    matchedTags: list[DebugTagItem]


class RecommendationItem(BaseModel):
    gameId: int
    name: LocalizedText
    steamUrl: str
    coverImageUrl: str | None = None
    reason: LocalizedText
    debug: DebugInfo | None = None


class RecommendRequest(BaseModel):
    answers: list[AnswerItem]


class DiagnosticsTagItem(BaseModel):
    tagCode: str
    score: int


class RecommendDiagnostics(BaseModel):
    llmEnabled: bool
    llmUsed: bool
    fallbackReason: str | None = None
    rerankChangedOrder: bool | None = None
    ruleCandidateGameIds: list[int]
    llmCandidateGameIds: list[int]
    finalGameIds: list[int]
    selectedTop3GameIds: list[int] | None = None
    userTopTags: list[DiagnosticsTagItem]


class RecommendResponse(BaseModel):
    recommendations: list[RecommendationItem]
    diagnostics: RecommendDiagnostics | None = None
