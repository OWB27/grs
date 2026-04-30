import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.settings import settings
from app.llm.prompts.reason_prompt import (
    REASON_PROMPT_VERSION,
    build_reason_developer_message,
    build_reason_user_message,
)
from app.schemas.llm_rerank import LLMReasonsInput, LLMReasonsOutput


logger = logging.getLogger(__name__)


def build_reason_generation_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", build_reason_developer_message()),
            ("user", "{reason_input_json}"),
        ]
    )

    model = ChatOpenAI(
        model=settings.LLM_RERANK_MODEL,
        api_key=settings.LLM_API_KEY,
        timeout=settings.LLM_RERANK_TIMEOUT_SECONDS,
        max_retries=settings.LLM_RERANK_MAX_RETRIES,
    )

    structured_model = model.with_structured_output(
        LLMReasonsOutput,
        method="json_schema",
        strict=True,
    )

    return prompt | structured_model


def call_llm_reason_generation(llm_input: LLMReasonsInput) -> LLMReasonsOutput:
    if not settings.LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY is not configured")

    chain = build_reason_generation_chain()
    logger.info(
        "calling llm reason generation model=%s candidate_count=%s timeout_seconds=%s max_retries=%s",
        settings.LLM_RERANK_MODEL,
        len(llm_input.candidates),
        settings.LLM_RERANK_TIMEOUT_SECONDS,
        settings.LLM_RERANK_MAX_RETRIES,
    )

    result = chain.invoke(
        {
            "reason_input_json": build_reason_user_message(llm_input),
        },
        config={
            "run_name": "GenerateRecommendationReasonsChain",
            "tags": ["grs", "llm", "reasons"],
            "metadata": {
                "model": settings.LLM_RERANK_MODEL,
                "prompt_version": REASON_PROMPT_VERSION,
                "candidate_count": len(llm_input.candidates),
                "profile_tag_count": len(llm_input.user_profile.top_tags),
            },
        }
    )

    if isinstance(result, LLMReasonsOutput):
        return result

    return LLMReasonsOutput.model_validate(result)
