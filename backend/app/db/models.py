from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Question(SQLModel, table=True):
    __tablename__ = "questions"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    sort_order: int

    title_zh: str
    title_en: str

    options: list["QuestionOption"] = Relationship(back_populates="question")


class QuestionOption(SQLModel, table=True):
    __tablename__ = "question_options"

    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="questions.id")
    code: str = Field(index=True, unique=True)
    sort_order: int

    text_zh: str
    text_en: str

    question: Optional[Question] = Relationship(back_populates="options")