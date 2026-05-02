import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.settings import settings
from app.llm.cache import build_llm_cache_key, llm_response_cache
from app.llm.prompts.reason_prompt import build_reason_developer_message, build_reason_user_message
from app.llm.prompts.registry import REASON_PROMPT_INFO
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

    cache_key = build_llm_cache_key(
        REASON_PROMPT_INFO.name,
        settings.LLM_RERANK_MODEL,
        REASON_PROMPT_INFO.version,
        llm_input,
    )
    if settings.LLM_CACHE_ENABLED:
        cached_result = llm_response_cache.get(cache_key)
        if cached_result is not None:
            logger.info("llm reason generation cache hit prompt_version=%s", REASON_PROMPT_INFO.version)
            return LLMReasonsOutput.model_validate(cached_result)

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
                "prompt_name": REASON_PROMPT_INFO.name,
                "prompt_version": REASON_PROMPT_INFO.version,
                "candidate_count": len(llm_input.candidates),
                "profile_tag_count": len(llm_input.user_profile.top_tags),
            },
        }
    )

    if isinstance(result, LLMReasonsOutput):
        if settings.LLM_CACHE_ENABLED:
            llm_response_cache.set(cache_key, result)
        return result

    validated_result = LLMReasonsOutput.model_validate(result)
    if settings.LLM_CACHE_ENABLED:
        llm_response_cache.set(cache_key, validated_result)

    return validated_result
