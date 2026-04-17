from typing import Literal

from pydantic import BaseModel, Field, field_validator


class LLMRerankTask(BaseModel):
    type: Literal["rerank_top_candidates"] = "rerank_top_candidates"
    candidate_limit: int = 15
    select_count: int = 3


class LLMUserProfileTag(BaseModel):
    tag_code: str
    tag_name_zh: str
    tag_name_en: str
    score: int = Field(ge=1)


class LLMUserProfile(BaseModel):
    top_tags: list[LLMUserProfileTag]


class LLMCandidateMatchedTag(BaseModel):
    tag_code: str
    tag_name_zh: str
    tag_name_en: str
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


class LLMSelectedGameReason(BaseModel):
    game_id: int
    reason_zh: str = Field(min_length=1)
    reason_en: str = Field(min_length=1)


class LLMRerankOutput(BaseModel):
    ranked_game_ids: list[int]
    top_3_reasons: list[LLMSelectedGameReason]

    @field_validator("ranked_game_ids")
    @classmethod
    def validate_ranked_game_ids_not_empty(cls, value: list[int]) -> list[int]:
        if not value:
            raise ValueError("ranked_game_ids must not be empty")
        return value

    @field_validator("top_3_reasons")
    @classmethod
    def validate_top_3_reasons_not_empty(cls, value: list[LLMSelectedGameReason]) -> list[LLMSelectedGameReason]:
        if not value:
            raise ValueError("top_3_reasons must not be empty")
        return value