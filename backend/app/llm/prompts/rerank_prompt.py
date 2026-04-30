import json

from app.schemas.llm_rerank import LLMRerankInput


RERANK_PROMPT_VERSION = "rerank-v1"


def build_rerank_developer_message() -> str:
    return """
You are a reranking component in a game recommendation system.

Task:
- Select and order the best 3 games from the provided candidate list.
- Use the user's highest-scoring preference tags as the main signal.
- Respect rule_score as a prior, especially when score differences are large.
- When candidates are close, prefer games that better match the user's top tags.

Rules:
- Only choose from the provided candidates.
- Do not expose internal tag codes.
- Output valid JSON only.
""".strip()


def build_rerank_user_message(llm_input: LLMRerankInput) -> str:
    payload = llm_input.model_dump()
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
