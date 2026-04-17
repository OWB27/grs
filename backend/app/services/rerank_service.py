from copy import deepcopy

from app.schemas.llm_rerank import (
    LLMCandidateItem,
    LLMCandidateMatchedTag,
    LLMRerankInput,
    LLMRerankOutput,
    LLMRerankTask,
    LLMSelectedGameReason,
    LLMUserProfile,
    LLMUserProfileTag,
)


def build_llm_rerank_input(top_candidates: list[dict], user_profile: dict[str, int]) -> LLMRerankInput:
    sorted_profile_items = sorted(
        user_profile.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    top_profile_tags = []
    for tag_code, score in sorted_profile_items[:5]:
        top_profile_tags.append(
            LLMUserProfileTag(
                tag_code=tag_code,
                tag_name_zh=tag_code,
                tag_name_en=tag_code,
                score=score,
            )
        )

    candidate_items = []
    for candidate in top_candidates:
        game = candidate["game"]

        matched_tags = []
        for item in candidate["matchedTags"][:4]:
            matched_tags.append(
                LLMCandidateMatchedTag(
                    tag_code=item["tagCode"],
                    tag_name_zh=item.get("tagNameZh", item["tagCode"]),
                    tag_name_en=item.get("tagNameEn", item["tagCode"]),
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


def call_fake_llm_rerank(llm_input: LLMRerankInput) -> LLMRerankOutput:
    sorted_candidates = sorted(
        llm_input.candidates,
        key=lambda item: (
            len(item.matched_tags),
            item.rule_score,
        ),
        reverse=True,
    )

    ranked_game_ids = [item.game_id for item in sorted_candidates]

    top_3 = sorted_candidates[:3]
    top_3_reasons = []

    for candidate in top_3:
        if candidate.matched_tags:
            top_tags = candidate.matched_tags[:2]
            zh_names = [tag.tag_name_zh for tag in top_tags]
            en_names = [tag.tag_name_en for tag in top_tags]

            if len(zh_names) == 1:
                zh_text = zh_names[0]
                en_text = en_names[0]
            else:
                zh_text = f"{zh_names[0]}、{zh_names[1]}"
                en_text = f"{en_names[0]} and {en_names[1]}"
        else:
            zh_text = "整体偏好"
            en_text = "overall preference"

        top_3_reasons.append(
            LLMSelectedGameReason(
                game_id=candidate.game_id,
                reason_zh=f"这款游戏在{zh_text}这些维度上与你的画像更匹配，因此被优先展示。",
                reason_en=f"This game aligns better with your profile on {en_text}, so it is prioritized for display.",
            )
        )

    return LLMRerankOutput(
        ranked_game_ids=ranked_game_ids,
        top_3_reasons=top_3_reasons,
    )


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
            "zh": item.reason_zh,
            "en": item.reason_en,
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


def rerank_candidates_with_fallback(top_candidates: list[dict], user_profile: dict[str, int]) -> dict:
    try:
        llm_input = build_llm_rerank_input(top_candidates, user_profile)
        llm_output = call_fake_llm_rerank(llm_input)

        candidate_ids = [candidate["game"].id for candidate in top_candidates]
        validate_llm_rerank_output(llm_output, candidate_ids)

        reranked_candidates = apply_llm_rerank(top_candidates, llm_output)

        return {
            "llm_used": True,
            "ranked_candidates": reranked_candidates,
            "fallback_reason": None,
        }
    except Exception:
        return {
            "llm_used": False,
            "ranked_candidates": top_candidates,
            "fallback_reason": "fake_llm_rerank_failed",
        }