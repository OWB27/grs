import logging
from copy import deepcopy

from sqlmodel import Session, select

from app.core.settings import settings
from app.core.tag_descriptions import TAG_DESCRIPTIONS
from app.db.models import Tag
from app.llm.quality_checks import (
    get_llm_output_hard_failures,
    get_llm_output_soft_warnings,
    get_reasons_output_hard_failures,
    get_rerank_output_hard_failures,
)
from app.llm.reason_client import call_llm_reason_generation
from app.llm.rerank_client import call_llm_rerank
from app.schemas.llm_rerank import (
    LLMCandidateItem,
    LLMCandidateMatchedTag,
    LLMReasonsInput,
    LLMReasonsOutput,
    LLMReasonsTask,
    LLMRerankInput,
    LLMRerankOutput,
    LLMRerankTask,
    LLMUserProfile,
    LLMUserProfileTag,
)
from app.schemas.recommend import RecommendDiagnostics


logger = logging.getLogger(__name__)


def build_recommend_diagnostics(
    *,
    llm_enabled: bool,
    llm_used: bool,
    fallback_reason: str | None,
    user_profile: dict[str, int],
    top_candidates: list[dict],
    llm_candidates: list[dict],
    ranked_candidates: list[dict],
    selected_top_3_game_ids: list[int] | None = None,
) -> RecommendDiagnostics:
    rule_candidate_game_ids = [
        candidate["game"].id
        for candidate in top_candidates
    ]
    llm_candidate_game_ids = [
        candidate["game"].id
        for candidate in llm_candidates
    ]
    final_game_ids = [
        candidate["game"].id
        for candidate in ranked_candidates
    ]
    sorted_profile_items = sorted(
        user_profile.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return RecommendDiagnostics(
        llmEnabled=llm_enabled,
        llmUsed=llm_used,
        fallbackReason=fallback_reason,
        rerankChangedOrder=rule_candidate_game_ids[:3] != final_game_ids[:3],
        ruleCandidateGameIds=rule_candidate_game_ids,
        llmCandidateGameIds=llm_candidate_game_ids,
        finalGameIds=final_game_ids,
        selectedTop3GameIds=selected_top_3_game_ids,
        userTopTags=[
            {
                "tagCode": tag_code,
                "score": score,
            }
            for tag_code, score in sorted_profile_items[: settings.LLM_PROFILE_TAG_COUNT]
        ],
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
    for tag_code, score in sorted_profile_items[: settings.LLM_PROFILE_TAG_COUNT]:
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
        for item in candidate["matchedTags"][: settings.LLM_MATCHED_TAG_COUNT]:
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
            type="select_top_3_from_candidates",
            candidate_limit=len(candidate_items),
            select_count=3,
        ),
        user_profile=LLMUserProfile(top_tags=top_profile_tags),
        candidates=candidate_items,
    )


def validate_llm_rerank_output(
    llm_input: LLMRerankInput,
    llm_output: LLMRerankOutput,
) -> None:
    hard_failures = get_rerank_output_hard_failures(llm_input, llm_output)
    if hard_failures:
        raise ValueError(f"LLM rerank output failed quality checks: {hard_failures}")


def build_llm_reasons_input(
    llm_input: LLMRerankInput,
    selected_top_3_game_ids: list[int],
) -> LLMReasonsInput:
    candidates_by_game_id = {
        candidate.game_id: candidate
        for candidate in llm_input.candidates
    }

    selected_candidates = [
        candidates_by_game_id[game_id]
        for game_id in selected_top_3_game_ids
    ]

    return LLMReasonsInput(
        task=LLMReasonsTask(),
        user_profile=llm_input.user_profile,
        candidates=selected_candidates,
    )


def validate_llm_reasons_output(
    llm_output: LLMRerankOutput,
    reasons_output: LLMReasonsOutput,
) -> None:
    hard_failures = get_reasons_output_hard_failures(llm_output, reasons_output)
    if hard_failures:
        raise ValueError(f"LLM reasons output failed quality checks: {hard_failures}")


def validate_llm_output_quality(
    llm_input: LLMRerankInput,
    llm_output: LLMRerankOutput,
    reasons_output: LLMReasonsOutput,
) -> None:
    hard_failures = get_llm_output_hard_failures(llm_input, llm_output, reasons_output)
    if hard_failures:
        raise ValueError(f"LLM output failed quality checks: {hard_failures}")

    soft_warnings = get_llm_output_soft_warnings(llm_input, reasons_output)
    if soft_warnings:
        logger.warning("llm output quality warnings=%s", soft_warnings)


def apply_llm_rerank(
    top_candidates: list[dict],
    llm_candidates: list[dict],
    llm_output: LLMRerankOutput,
    reasons_output: LLMReasonsOutput,
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
        for item in reasons_output.top_3_reasons
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
    logger.info(
        "rerank start enabled=%s model=%s llm_api_key_loaded=%s candidate_count=%s",
        settings.LLM_RERANK_ENABLED,
        settings.LLM_RERANK_MODEL,
        bool(settings.LLM_API_KEY),
        len(top_candidates),
    )

    if not settings.LLM_RERANK_ENABLED:
        logger.info("rerank fallback reason=llm_disabled")
        return {
            "llm_used": False,
            "ranked_candidates": top_candidates,
            "fallback_reason": "llm_disabled",
            "diagnostics": build_recommend_diagnostics(
                llm_enabled=False,
                llm_used=False,
                fallback_reason="llm_disabled",
                user_profile=user_profile,
                top_candidates=top_candidates,
                llm_candidates=[],
                ranked_candidates=top_candidates,
            ),
        }

    llm_candidates: list[dict] = []
    selected_top_3_game_ids: list[int] | None = None

    try:
        llm_candidates = top_candidates[: settings.LLM_RERANK_CANDIDATE_COUNT]
        tag_metadata_lookup = build_tag_metadata_lookup(session)
        llm_input = build_llm_rerank_input(
            llm_candidates,
            user_profile,
            tag_metadata_lookup,
        )
        logger.info("llm rerank input built candidate_count=%s", len(llm_candidates))

        llm_output = call_llm_rerank(llm_input)
        selected_top_3_game_ids = llm_output.selected_top_3_game_ids
        logger.info(
            "llm rerank output received selected_top_3_game_ids=%s",
            selected_top_3_game_ids,
        )

        validate_llm_rerank_output(llm_input, llm_output)
        logger.info("llm rerank output validated")

        reasons_input = build_llm_reasons_input(
            llm_input,
            llm_output.selected_top_3_game_ids,
        )
        logger.info("llm reasons input built candidate_count=%s", len(reasons_input.candidates))

        reasons_output = call_llm_reason_generation(reasons_input)
        logger.info("llm reasons output received")

        validate_llm_reasons_output(llm_output, reasons_output)
        logger.info("llm reasons output validated")

        validate_llm_output_quality(llm_input, llm_output, reasons_output)
        logger.info("llm output quality checked")

        reranked_candidates = apply_llm_rerank(
            top_candidates,
            llm_candidates,
            llm_output,
            reasons_output,
        )
        logger.info("llm rerank applied")

        return {
            "llm_used": True,
            "ranked_candidates": reranked_candidates,
            "fallback_reason": None,
            "diagnostics": build_recommend_diagnostics(
                llm_enabled=True,
                llm_used=True,
                fallback_reason=None,
                user_profile=user_profile,
                top_candidates=top_candidates,
                llm_candidates=llm_candidates,
                ranked_candidates=reranked_candidates,
                selected_top_3_game_ids=selected_top_3_game_ids,
            ),
        }
    except Exception as error:
        logger.exception("rerank fallback reason=llm_rerank_failed error=%r", error)

        return {
            "llm_used": False,
            "ranked_candidates": top_candidates,
            "fallback_reason": "llm_rerank_failed",
            "diagnostics": build_recommend_diagnostics(
                llm_enabled=True,
                llm_used=False,
                fallback_reason="llm_rerank_failed",
                user_profile=user_profile,
                top_candidates=top_candidates,
                llm_candidates=llm_candidates,
                ranked_candidates=top_candidates,
                selected_top_3_game_ids=selected_top_3_game_ids,
            ),
        }
