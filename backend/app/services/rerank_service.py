import json
from copy import deepcopy

from openai import OpenAI
from sqlmodel import Session, select

from app.core.settings import settings
from app.core.tag_descriptions import TAG_DESCRIPTIONS
from app.db.models import Tag
from app.schemas.llm_rerank import (
    LLMCandidateItem,
    LLMCandidateMatchedTag,
    LLMRerankInput,
    LLMRerankOutput,
    LLMRerankTask,
    LLMUserProfile,
    LLMUserProfileTag,
)


def build_tag_metadata_lookup(session: Session) -> dict[str, dict[str, str]]:
    tags = session.exec(select(Tag)).all()

    result: dict[str, dict[str, str]] = {}
    for tag in tags:
        description = TAG_DESCRIPTIONS.get(
            tag.code,
            {
                "zh": tag.name_zh,
                "en": tag.name_en,
            },
        )

        result[tag.code] = {
            "zh": tag.name_zh,
            "en": tag.name_en,
            "description_zh": description["zh"],
            "description_en": description["en"],
        }

    return result


def build_llm_rerank_input(
    llm_candidates: list[dict],
    user_profile: dict[str, int],
    tag_metadata_lookup: dict[str, dict[str, str]],
) -> LLMRerankInput:
    sorted_profile_items = sorted(
        user_profile.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    top_profile_tags = []
    for tag_code, score in sorted_profile_items[:5]:
        meta = tag_metadata_lookup.get(
            tag_code,
            {
                "zh": tag_code,
                "en": tag_code,
                "description_zh": tag_code,
                "description_en": tag_code,
            },
        )

        top_profile_tags.append(
            LLMUserProfileTag(
                tag_code=tag_code,
                tag_name_zh=meta["zh"],
                tag_name_en=meta["en"],
                tag_description_zh=meta["description_zh"],
                tag_description_en=meta["description_en"],
                score=score,
            )
        )

    candidate_items = []
    for candidate in llm_candidates:
        game = candidate["game"]

        matched_tags = []
        for item in candidate["matchedTags"][:3]:
            tag_code = item["tagCode"]
            meta = tag_metadata_lookup.get(
                tag_code,
                {
                    "zh": tag_code,
                    "en": tag_code,
                    "description_zh": tag_code,
                    "description_en": tag_code,
                },
            )

            matched_tags.append(
                LLMCandidateMatchedTag(
                    tag_code=tag_code,
                    tag_name_zh=item.get("tagNameZh", meta["zh"]),
                    tag_name_en=item.get("tagNameEn", meta["en"]),
                    tag_description_zh=meta["description_zh"],
                    tag_description_en=meta["description_en"],
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
            type="select_top_3_from_top_6",
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


def build_developer_message() -> str:
    return """
You are a reranking component in a game recommendation system.

Task:
- Select and order the best 3 games from the provided candidate list.
- Use the user's highest-scoring preference tags as the main signal.
- Respect rule_score as a prior, especially when score differences are large.
- When candidates are close, prefer games that better match the user's top tags.
- Write short, natural reasons for the selected top 3.

Rules:
- Only choose from the provided candidates.
- reason.zh must be fully in Simplified Chinese.
- reason.en must be fully in English.
- Keep reasons short and user-facing.
- Do not expose internal tag codes.
- Output valid JSON only.
""".strip()


def build_user_message(llm_input: LLMRerankInput) -> str:
    payload = llm_input.model_dump()
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


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


def validate_llm_rerank_output(
    llm_output: LLMRerankOutput,
    candidate_ids: list[int],
) -> None:
    selected_ids = llm_output.selected_top_3_game_ids

    if len(set(selected_ids)) != 3:
        raise ValueError("selected_top_3_game_ids contains duplicates")

    if not set(selected_ids).issubset(set(candidate_ids)):
        raise ValueError("selected_top_3_game_ids must be chosen from candidate ids")

    reason_ids = [item.game_id for item in llm_output.top_3_reasons]
    if reason_ids != selected_ids:
        raise ValueError("top_3_reasons must match selected_top_3_game_ids in order")


def apply_llm_rerank(
    top_candidates: list[dict],
    llm_candidates: list[dict],
    llm_output: LLMRerankOutput,
) -> list[dict]:
    top_candidates_by_game_id = {
        candidate["game"].id: deepcopy(candidate)
        for candidate in top_candidates
    }

    llm_candidate_ids = [candidate["game"].id for candidate in llm_candidates]
    selected_top_3_ids = llm_output.selected_top_3_game_ids

    reasons_by_game_id = {
        item.game_id: {
            "zh": item.reason.zh,
            "en": item.reason.en,
        }
        for item in llm_output.top_3_reasons
    }

    final_candidates = []

    for game_id in selected_top_3_ids:
        candidate = top_candidates_by_game_id[game_id]
        candidate["reason"] = reasons_by_game_id[game_id]
        candidate["rankingMode"] = "llm_reranked"
        final_candidates.append(candidate)

    selected_set = set(selected_top_3_ids)

    remaining_llm_ids = [
        game_id for game_id in llm_candidate_ids
        if game_id not in selected_set
    ]
    remaining_rule_ids = [
        candidate["game"].id
        for candidate in top_candidates
        if candidate["game"].id not in selected_set
        and candidate["game"].id not in set(remaining_llm_ids)
    ]

    for game_id in remaining_llm_ids + remaining_rule_ids:
        candidate = top_candidates_by_game_id[game_id]
        candidate["rankingMode"] = "rule_based"
        final_candidates.append(candidate)

    return final_candidates


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
        llm_candidates = top_candidates[:6]
        candidate_ids = [candidate["game"].id for candidate in llm_candidates]

        tag_metadata_lookup = build_tag_metadata_lookup(session)
        llm_input = build_llm_rerank_input(
            llm_candidates,
            user_profile,
            tag_metadata_lookup,
        )
        print("llm_input built")

        llm_output = call_openai_llm_rerank(llm_input)
        print("llm_output received")
        print("selected_top_3_game_ids =", llm_output.selected_top_3_game_ids)

        validate_llm_rerank_output(llm_output, candidate_ids)
        print("llm_output validated")

        reranked_candidates = apply_llm_rerank(
            top_candidates,
            llm_candidates,
            llm_output,
        )
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
