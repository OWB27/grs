from dataclasses import dataclass

from app.llm.prompts.reason_prompt import REASON_PROMPT_VERSION
from app.llm.prompts.rerank_prompt import RERANK_PROMPT_VERSION


@dataclass(frozen=True)
class PromptInfo:
    name: str
    version: str
    purpose: str
    change_note: str


RERANK_PROMPT_INFO = PromptInfo(
    name="rerank",
    version=RERANK_PROMPT_VERSION,
    purpose="Select and order the best 3 games from the LLM candidate set.",
    change_note="Initial LangChain rerank prompt after splitting reasons into a separate chain.",
)

REASON_PROMPT_INFO = PromptInfo(
    name="reason_generation",
    version=REASON_PROMPT_VERSION,
    purpose="Generate short bilingual recommendation reasons for the selected top 3 games.",
    change_note="Initial LangChain reason prompt after splitting rerank into a separate chain.",
)


PROMPT_REGISTRY = {
    RERANK_PROMPT_INFO.name: RERANK_PROMPT_INFO,
    REASON_PROMPT_INFO.name: REASON_PROMPT_INFO,
}
