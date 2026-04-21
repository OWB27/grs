from typing import Literal

from pydantic import BaseModel, Field, field_validator


class LLMRerankTask(BaseModel):
    type: Literal["select_top_3_from_top_6"] = "select_top_3_from_top_6"
    candidate_limit: int = 6
    select_count: int = 3


class LLMUserProfileTag(BaseModel):
    tag_code: str
    tag_name_zh: str
    tag_name_en: str
    tag_description_zh: str
    tag_description_en: str
    score: int = Field(ge=1)


class LLMUserProfile(BaseModel):
    top_tags: list[LLMUserProfileTag]


class LLMCandidateMatchedTag(BaseModel):
    tag_code: str
    tag_name_zh: str
    tag_name_en: str
    tag_description_zh: str
    tag_description_en: str
    contribution: int = Field(ge=1)


class LLMCandidateItem(BaseModel):
    game_id: int
    name_zh: str
    name_en: str
    rule_score: float = Field(ge=0)
    matched_tags: list[LLMCandidateMatchedTag]


class LLMRerankInput(BaseModel):
    task: LLMRerankTask
    user_profile: LLMUserProfile
    candidates: list[LLMCandidateItem]

    @field_validator("candidates")
    @classmethod
    def validate_candidates_not_empty(cls, value: list[LLMCandidateItem]) -> list[LLMCandidateItem]:
        if not value:
            raise ValueError("candidates must not be empty")
        return value


class LLMReasonText(BaseModel):
    zh: str = Field(min_length=1, max_length=60)
    en: str = Field(min_length=1, max_length=160)


class LLMSelectedGameReason(BaseModel):
    game_id: int
    reason: LLMReasonText


class LLMRerankOutput(BaseModel):
    selected_top_3_game_ids: list[int]
    top_3_reasons: list[LLMSelectedGameReason]

    @field_validator("selected_top_3_game_ids")
    @classmethod
    def validate_selected_top_3_game_ids(cls, value: list[int]) -> list[int]:
        if len(value) != 3:
            raise ValueError("selected_top_3_game_ids must contain exactly 3 items")
        if len(set(value)) != 3:
            raise ValueError("selected_top_3_game_ids must not contain duplicates")
        return value

    @field_validator("top_3_reasons")
    @classmethod
    def validate_top_3_reasons_not_empty(cls, value: list[LLMSelectedGameReason]) -> list[LLMSelectedGameReason]:
        if len(value) != 3:
            raise ValueError("top_3_reasons must contain exactly 3 items")
        return value