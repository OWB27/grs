from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship


# ----------------------
# 已有表（示意）
# ----------------------

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
    tag_weights: list["OptionTagWeight"] = Relationship(back_populates="option")


# ----------------------
# 新增表 1：games
# ----------------------

class Game(SQLModel, table=True):
    __tablename__ = "games"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)

    name_zh: str
    name_en: str

    steam_url: str
    cover_image_url: Optional[str] = None

    is_active: bool = Field(default=True)

    game_tags: list["GameTag"] = Relationship(back_populates="game")


# ----------------------
# 新增表 2：tags
# ----------------------

class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)

    name_zh: str
    name_en: str

    is_active: bool = Field(default=True)

    game_tags: list["GameTag"] = Relationship(back_populates="tag")
    option_tag_weights: list["OptionTagWeight"] = Relationship(back_populates="tag")


# ----------------------
# 新增表 3：game_tags
# ----------------------

class GameTag(SQLModel, table=True):
    __tablename__ = "game_tags"
    __table_args__ = (
        UniqueConstraint("game_id", "tag_id", name="uq_game_tags_game_id_tag_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    game_id: int = Field(foreign_key="games.id")
    tag_id: int = Field(foreign_key="tags.id")

    weight: int

    game: Optional[Game] = Relationship(back_populates="game_tags")
    tag: Optional[Tag] = Relationship(back_populates="game_tags")


# ----------------------
# 新增表 4：option_tag_weights
# ----------------------

class OptionTagWeight(SQLModel, table=True):
    __tablename__ = "option_tag_weights"

    id: Optional[int] = Field(default=None, primary_key=True)

    option_id: int = Field(foreign_key="question_options.id")
    tag_id: int = Field(foreign_key="tags.id")

    weight: int

    option: Optional[QuestionOption] = Relationship(back_populates="tag_weights")
    tag: Optional[Tag] = Relationship(back_populates="option_tag_weights")
