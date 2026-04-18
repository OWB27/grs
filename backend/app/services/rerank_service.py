import json
from copy import deepcopy

from openai import OpenAI
from sqlmodel import Session, select

from app.core.settings import settings
from app.db.models import Tag
from app.schemas.llm_rerank import (
    LLMCandidateItem,
    LLMCandidateMatchedTag,
    LLMReasonText,
    LLMRerankInput,
    LLMRerankOutput,
    LLMRerankTask,
    LLMSelectedGameReason,
    LLMUserProfile,
    LLMUserProfileTag,
)

def build_tag_label_lookup(session: Session) -> dict[str, dict[str, str]]:
    tags = session.exec(select(Tag)).all()

    return {
        tag.code: {
            "zh": tag.name_zh,
            "en": tag.name_en,
        }
        for tag in tags
    }

def build_llm_rerank_input(
    top_candidates: list[dict],
    user_profile: dict[str, int],
    tag_label_lookup: dict[str, dict[str, str]],
) -> LLMRerankInput:
    sorted_profile_items = sorted(
        user_profile.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    top_profile_tags = []
    for tag_code, score in sorted_profile_items[:5]:
        label = tag_label_lookup.get(
            tag_code,
            {
                "zh": tag_code,
                "en": tag_code,
            },
        )

        top_profile_tags.append(
            LLMUserProfileTag(
                tag_code=tag_code,
                tag_name_zh=label["zh"],
                tag_name_en=label["en"],
                score=score,
            )
        )

    candidate_items = []
    for candidate in top_candidates:
        game = candidate["game"]

        matched_tags = []
        for item in candidate["matchedTags"][:4]:
            tag_code = item["tagCode"]

            label = tag_label_lookup.get(
                tag_code,
                {
                    "zh": tag_code,
                    "en": tag_code,
                },
            )

            matched_tags.append(
                LLMCandidateMatchedTag(
                    tag_code=tag_code,
                    tag_name_zh=item.get("tagNameZh", label["zh"]),
                    tag_name_en=item.get("tagNameEn", label["en"]),
                    contribution=item["contribution"],
                )
            )

        candidate_items.append(
            LLMCandidateItem(
                game_id=game.id,
                name_zh=game.name_zh,
                name_en=game.name_en,
                rule_score=candidate["score"],
                matched_tags=matched_tags,
            )
        )

    return LLMRerankInput(
        task=LLMRerankTask(
            type="rerank_top_candidates",
            candidate_limit=len(candidate_items),
            select_count=3,
        ),
        user_profile=LLMUserProfile(top_tags=top_profile_tags),
        candidates=candidate_items,
    )


def get_llm_rerank_output_schema() -> dict:
    return {
        "name": "llm_rerank_output",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "ranked_game_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
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
                },
            },
            "required": ["ranked_game_ids", "top_3_reasons"],
            "additionalProperties": False,
        },
    }


def build_developer_message() -> str:
    return """
You are a reranking component inside a game recommendation backend.

Your job:
1. Re-rank the provided candidate games only.
2. Return a full ordered list of candidate game IDs.
3. Provide natural reasons for the top 3 games only.

Primary ranking goal:
- Prioritize the user's highest-scoring preference tags.
- Treat the user's top preference tags as the most important signal for final display order.
- Use matched tag contributions to judge how strongly each candidate aligns with the user's profile.
- Pay special attention to the top 3 user preference tags. These should influence ranking more than lower-priority tags.

How to use rule_score:
- The existing rule_score is an important prior signal and should usually be respected.
- Do not ignore rule_score without a good reason.
- When one game is clearly stronger in rule_score, keep the stronger rule-based ordering unless another candidate is meaningfully better aligned with the user's top preference tags.
- When two or more games have similar rule_score, use the user's highest-priority tags to make a finer reranking decision.
- In close-score situations, prefer the candidate whose strongest matched tags better reflect the user's core preferences.

How to rerank:
- Keep the ranking conservative and grounded.
- Do not reorder aggressively without clear evidence from the user's top preference tags and candidate matched tags.
- Make small, preference-sensitive adjustments rather than arbitrary reshuffling.
- Favor candidates whose top matched tags overlap strongly with the user's most important preference tags.
- If a candidate mainly matches lower-priority user tags, do not rank it above a candidate that better matches the user's top-priority tags unless the evidence is clearly stronger.

Reason-writing rules:
- Explain the recommendation in user-facing language.
- Focus on why the game matches the user's strongest preferences.
- Avoid repeating raw internal scoring language.
- Avoid exposing internal tag codes directly.

Language rules:
- reason.zh must be written entirely in Simplified Chinese.
- reason.en must be written entirely in English.
- Do not mix Chinese and English in the same field.
- Do not output internal tag codes like story_rich, immersive, or exploration directly.
- Convert tag meanings into natural user-facing language.

Hard constraints:
- You must only use game IDs from the provided candidate list.
- ranked_game_ids must contain every candidate exactly once.
- top_3_reasons must correspond exactly to the first 3 game IDs in ranked_game_ids.
- Do not invent new games.
- Do not add extra fields.
- Output valid JSON only.
""".strip()


def build_user_message(llm_input: LLMRerankInput) -> str:
    payload = llm_input.model_dump()
    return json.dumps(payload, ensure_ascii=False, indent=2)


def call_openai_llm_rerank(llm_input: LLMRerankInput) -> LLMRerankOutput:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=settings.OPENAI_RERANK_MODEL,
        messages=[
            {
                "role": "developer",
                "content": build_developer_message(),
            },
            {
                "role": "user",
                "content": build_user_message(llm_input),
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


def validate_llm_rerank_output(llm_output: LLMRerankOutput, candidate_ids: list[int]) -> None:
    ranked_ids = llm_output.ranked_game_ids

    if len(ranked_ids) != len(candidate_ids):
        raise ValueError("ranked_game_ids length does not match candidate count")

    if len(set(ranked_ids)) != len(ranked_ids):
        raise ValueError("ranked_game_ids contains duplicates")

    if set(ranked_ids) != set(candidate_ids):
        raise ValueError("ranked_game_ids must exactly match candidate ids")

    top_3_ids = ranked_ids[:3]
    reason_ids = [item.game_id for item in llm_output.top_3_reasons]

    if len(reason_ids) != 3:
        raise ValueError("top_3_reasons must contain exactly 3 items")

    if reason_ids != top_3_ids:
        raise ValueError("top_3_reasons must match the first 3 ranked game ids")


def apply_llm_rerank(top_candidates: list[dict], llm_output: LLMRerankOutput) -> list[dict]:
    candidates_by_game_id = {
        candidate["game"].id: deepcopy(candidate)
        for candidate in top_candidates
    }

    reasons_by_game_id = {
        item.game_id: {
            "zh": item.reason.zh,
            "en": item.reason.en,
        }
        for item in llm_output.top_3_reasons
    }

    reranked_candidates = []
    for game_id in llm_output.ranked_game_ids:
        candidate = candidates_by_game_id[game_id]

        if game_id in reasons_by_game_id:
            candidate["reason"] = reasons_by_game_id[game_id]

        reranked_candidates.append(candidate)

    return reranked_candidates

def rerank_candidates_with_fallback(
    session: Session,
    top_candidates: list[dict],
    user_profile: dict[str, int],
) -> dict:
    print("=== RERANK START ===")
    print("OPENAI_RERANK_ENABLED =", settings.OPENAI_RERANK_ENABLED)
    print("OPENAI_RERANK_MODEL =", settings.OPENAI_RERANK_MODEL)
    print("OPENAI_API_KEY loaded =", bool(settings.OPENAI_API_KEY))
    print("candidate_count =", len(top_candidates))

    if not settings.OPENAI_RERANK_ENABLED:
        print("fallback: llm_disabled")
        return {
            "llm_used": False,
            "ranked_candidates": top_candidates,
            "fallback_reason": "llm_disabled",
        }

    try:
        tag_label_lookup = build_tag_label_lookup(session)
        llm_input = build_llm_rerank_input(
            top_candidates,
            user_profile,
            tag_label_lookup,
        )
        print("llm_input built")

        llm_output = call_openai_llm_rerank(llm_input)
        print("llm_output received")
        print("ranked_game_ids =", llm_output.ranked_game_ids)
        print("top_3_reason_ids =", [item.game_id for item in llm_output.top_3_reasons])

        candidate_ids = [candidate["game"].id for candidate in top_candidates]
        print("candidate_ids =", candidate_ids)

        validate_llm_rerank_output(llm_output, candidate_ids)
        print("llm_output validated")

        reranked_candidates = apply_llm_rerank(top_candidates, llm_output)
        print("rerank applied")

        return {
            "llm_used": True,
            "ranked_candidates": reranked_candidates,
            "fallback_reason": None,
        }
    except Exception as error:
        print("=== RERANK FAILED ===")
        print(repr(error))

        return {
            "llm_used": False,
            "ranked_candidates": top_candidates,
            "fallback_reason": "llm_rerank_failed",
        }