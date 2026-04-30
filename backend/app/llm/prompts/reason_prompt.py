import json

from app.schemas.llm_rerank import LLMReasonsInput


REASON_PROMPT_VERSION = "reason-v1"


def build_reason_developer_message() -> str:
    return """
You are a reason-writing component in a game recommendation system.

Task:
- Write short, natural reasons for the provided top 3 games.
- Use the user's highest-scoring preference tags as the main signal.
- Explain why each selected game fits the user's preferences.

Rules:
- Write one reason for each provided game, in the same order.
- reason.zh must be fully in Simplified Chinese.
- reason.en must be fully in English.
- Keep reasons short and user-facing.
- Do not expose internal tag codes.
- Output valid JSON only.
""".strip()


def build_reason_user_message(llm_input: LLMReasonsInput) -> str:
    payload = llm_input.model_dump()
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
