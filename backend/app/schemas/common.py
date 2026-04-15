from pydantic import BaseModel


class LocalizedText(BaseModel):
    zh: str
    en: str
