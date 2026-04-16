from pydantic import BaseModel


class LocalizedText(BaseModel):
    zh: str
    en: str

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    error: ErrorDetail