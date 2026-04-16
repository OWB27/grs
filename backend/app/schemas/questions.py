from pydantic import BaseModel

from app.schemas.common import LocalizedText


class QuestionOptionItem(BaseModel):
    id: int
    code: str
    sortOrder: int
    text: LocalizedText


class QuestionItem(BaseModel):
    id: int
    code: str
    sortOrder: int
    title: LocalizedText
    options: list[QuestionOptionItem]


class QuestionsResponse(BaseModel):
    questions: list[QuestionItem]