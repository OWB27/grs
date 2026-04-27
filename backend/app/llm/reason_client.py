import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.settings import settings
from app.llm.prompts.reason_prompt import (
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
        model=settings.OPENAI_RERANK_MODEL,
        api_key=settings.OPENAI_API_KEY,
        timeout=settings.OPENAI_RERANK_TIMEOUT_SECONDS,
        max_retries=settings.OPENAI_RERANK_MAX_RETRIES,
    )

    structured_model = model.with_structured_output(
        LLMReasonsOutput,
        method="json_schema",
        strict=True,
    )

    return prompt | structured_model


def call_llm_reason_generation(llm_input: LLMReasonsInput) -> LLMReasonsOutput:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    chain = build_reason_generation_chain()
    logger.info(
        "calling llm reason generation model=%s candidate_count=%s timeout_seconds=%s max_retries=%s",
        settings.OPENAI_RERANK_MODEL,
        len(llm_input.candidates),
        settings.OPENAI_RERANK_TIMEOUT_SECONDS,
        settings.OPENAI_RERANK_MAX_RETRIES,
    )

    result = chain.invoke(
        {
            "reason_input_json": build_reason_user_message(llm_input),
        }
    )

    if isinstance(result, LLMReasonsOutput):
        return result

    return LLMReasonsOutput.model_validate(result)
