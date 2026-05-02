import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.settings import settings
from app.llm.cache import build_llm_cache_key, llm_response_cache
from app.llm.prompts.registry import RERANK_PROMPT_INFO
from app.llm.prompts.rerank_prompt import build_rerank_developer_message, build_rerank_user_message
from app.schemas.llm_rerank import LLMRerankInput, LLMRerankOutput


logger = logging.getLogger(__name__)


def build_rerank_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", build_rerank_developer_message()),
            ("user", "{rerank_input_json}"),
        ]
    )

    model = ChatOpenAI(
        model=settings.LLM_RERANK_MODEL,
        api_key=settings.LLM_API_KEY,
        timeout=settings.LLM_RERANK_TIMEOUT_SECONDS,
        max_retries=settings.LLM_RERANK_MAX_RETRIES,
    )

    structured_model = model.with_structured_output(
        LLMRerankOutput,
        method="json_schema",
        strict=True,
    )

    return prompt | structured_model


def call_llm_rerank(llm_input: LLMRerankInput) -> LLMRerankOutput:
    if not settings.LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY is not configured")

    cache_key = build_llm_cache_key(
        RERANK_PROMPT_INFO.name,
        settings.LLM_RERANK_MODEL,
        RERANK_PROMPT_INFO.version,
        llm_input,
    )
    if settings.LLM_CACHE_ENABLED:
        cached_result = llm_response_cache.get(cache_key)
        if cached_result is not None:
            logger.info("llm rerank cache hit prompt_version=%s", RERANK_PROMPT_INFO.version)
            return LLMRerankOutput.model_validate(cached_result)

    chain = build_rerank_chain()
    logger.info(
        "calling llm rerank model=%s candidate_count=%s timeout_seconds=%s max_retries=%s",
        settings.LLM_RERANK_MODEL,
        len(llm_input.candidates),
        settings.LLM_RERANK_TIMEOUT_SECONDS,
        settings.LLM_RERANK_MAX_RETRIES,
    )

    result = chain.invoke(
        {
            "rerank_input_json": build_rerank_user_message(llm_input),
        },
        config={
            "run_name": "RerankCandidatesChain",
            "tags": ["grs", "llm", "rerank"],
            "metadata": {
                "model": settings.LLM_RERANK_MODEL,
                "prompt_name": RERANK_PROMPT_INFO.name,
                "prompt_version": RERANK_PROMPT_INFO.version,
                "candidate_count": len(llm_input.candidates),
                "profile_tag_count": len(llm_input.user_profile.top_tags),
            },
        }
    )

    if isinstance(result, LLMRerankOutput):
        if settings.LLM_CACHE_ENABLED:
            llm_response_cache.set(cache_key, result)
        return result

    validated_result = LLMRerankOutput.model_validate(result)
    if settings.LLM_CACHE_ENABLED:
        llm_response_cache.set(cache_key, validated_result)

    return validated_result
