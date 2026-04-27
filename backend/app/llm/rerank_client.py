import json

from openai import OpenAI

from app.core.settings import settings
from app.llm.prompts.rerank_prompt import (
    build_rerank_developer_message,
    build_rerank_user_message,
)
from app.schemas.llm_rerank import LLMRerankInput, LLMRerankOutput


def get_llm_rerank_output_schema() -> dict:
    return {
        "name": "llm_rerank_output",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "selected_top_3_game_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "minItems": 3,
                    "maxItems": 3,
                },
                "top_3_reasons": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "game_id": {"type": "integer"},
                            "reason": {
                                "type": "object",
                                "properties": {
                                    "zh": {"type": "string"},
                                    "en": {"type": "string"},
                                },
                                "required": ["zh", "en"],
                                "additionalProperties": False,
                            },
                        },
                        "required": ["game_id", "reason"],
                        "additionalProperties": False,
                    },
                    "minItems": 3,
                    "maxItems": 3,
                },
            },
            "required": ["selected_top_3_game_ids", "top_3_reasons"],
            "additionalProperties": False,
        },
    }


def call_openai_llm_rerank(llm_input: LLMRerankInput) -> LLMRerankOutput:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=settings.OPENAI_RERANK_MODEL,
        messages=[
            {
                "role": "developer",
                "content": build_rerank_developer_message(),
            },
            {
                "role": "user",
                "content": build_rerank_user_message(llm_input),
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": get_llm_rerank_output_schema(),
        },
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("LLM returned empty content")

    parsed = json.loads(content)
    return LLMRerankOutput.model_validate(parsed)
