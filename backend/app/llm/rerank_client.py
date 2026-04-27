from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.settings import settings
from app.llm.prompts.rerank_prompt import (
    build_rerank_developer_message,
    build_rerank_user_message,
)
from app.schemas.llm_rerank import LLMRerankInput, LLMRerankOutput


def build_rerank_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", build_rerank_developer_message()),
            ("user", "{rerank_input_json}"),
        ]
    )

    model = ChatOpenAI(
        model=settings.OPENAI_RERANK_MODEL,
        api_key=settings.OPENAI_API_KEY,
    )

    structured_model = model.with_structured_output(
        LLMRerankOutput,
        method="json_schema",
        strict=True,
    )

    return prompt | structured_model


def call_llm_rerank(llm_input: LLMRerankInput) -> LLMRerankOutput:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    chain = build_rerank_chain()
    result = chain.invoke(
        {
            "rerank_input_json": build_rerank_user_message(llm_input),
        }
    )

    if isinstance(result, LLMRerankOutput):
        return result

    return LLMRerankOutput.model_validate(result)
