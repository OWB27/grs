import argparse
import json
import time
from pathlib import Path
from typing import Any

from app.llm.reason_client import call_llm_reason_generation
from app.llm.rerank_client import call_llm_rerank
from app.llm.evals.sample_cases import EVAL_CASES
from app.llm.prompts.registry import REASON_PROMPT_INFO, RERANK_PROMPT_INFO
from app.schemas.llm_rerank import LLMReasonsInput, LLMReasonsTask, LLMRerankInput


def _build_reasons_input(
    rerank_input: LLMRerankInput,
    selected_top_3_game_ids: list[int],
) -> LLMReasonsInput:
    candidates_by_game_id = {
        candidate.game_id: candidate
        for candidate in rerank_input.candidates
    }
    selected_candidates = [
        candidates_by_game_id[game_id]
        for game_id in selected_top_3_game_ids
    ]

    return LLMReasonsInput(
        task=LLMReasonsTask(),
        user_profile=rerank_input.user_profile,
        candidates=selected_candidates,
    )


def _contains_any(text: str, values: list[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def _internal_tag_codes(tag_codes: list[str]) -> list[str]:
    return [
        tag_code
        for tag_code in tag_codes
        if "_" in tag_code
    ]


def _contains_cjk(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def _looks_complete_sentence(text: str) -> bool:
    stripped = text.strip()
    return stripped.endswith((".", "!", "?"))


def _evaluate_result(
    rerank_input: LLMRerankInput,
    selected_top_3_game_ids: list[int],
    reasons: list[dict[str, Any]],
) -> list[str]:
    warnings: list[str] = []
    candidate_ids = [candidate.game_id for candidate in rerank_input.candidates]
    top_tag_codes = _internal_tag_codes(
        [tag.tag_code for tag in rerank_input.user_profile.top_tags]
    )

    if len(selected_top_3_game_ids) != 3:
        warnings.append("selected_top_3_game_ids_count_is_not_3")

    if len(set(selected_top_3_game_ids)) != len(selected_top_3_game_ids):
        warnings.append("selected_top_3_game_ids_contains_duplicates")

    if not set(selected_top_3_game_ids).issubset(set(candidate_ids)):
        warnings.append("selected_top_3_game_ids_contains_unknown_candidate")

    reason_ids = [item["game_id"] for item in reasons]
    if reason_ids != selected_top_3_game_ids:
        warnings.append("reason_ids_do_not_match_selected_order")

    for item in reasons:
        reason = item["reason"]
        if not reason.get("zh"):
            warnings.append(f"empty_zh_reason_for_game_{item['game_id']}")
        if not reason.get("en"):
            warnings.append(f"empty_en_reason_for_game_{item['game_id']}")
        if _contains_cjk(reason.get("en", "")):
            warnings.append(f"en_reason_contains_chinese_for_game_{item['game_id']}")
        if reason.get("en") and not _looks_complete_sentence(reason["en"]):
            warnings.append(f"en_reason_may_be_incomplete_for_game_{item['game_id']}")
        if _contains_any(reason.get("zh", ""), top_tag_codes) or _contains_any(reason.get("en", ""), top_tag_codes):
            warnings.append(f"reason_exposes_tag_code_for_game_{item['game_id']}")

    return warnings


def _run_case(case_name: str, rerank_input: LLMRerankInput) -> dict[str, Any]:
    rerank_started_at = time.perf_counter()
    rerank_output = call_llm_rerank(rerank_input)
    rerank_latency_ms = round((time.perf_counter() - rerank_started_at) * 1000)

    reasons_input = _build_reasons_input(
        rerank_input,
        rerank_output.selected_top_3_game_ids,
    )
    reasons_started_at = time.perf_counter()
    reasons_output = call_llm_reason_generation(reasons_input)
    reasons_latency_ms = round((time.perf_counter() - reasons_started_at) * 1000)

    reasons = [
        item.model_dump()
        for item in reasons_output.top_3_reasons
    ]
    warnings = _evaluate_result(
        rerank_input,
        rerank_output.selected_top_3_game_ids,
        reasons,
    )

    return {
        "case_name": case_name,
        "prompt_versions": {
            RERANK_PROMPT_INFO.name: RERANK_PROMPT_INFO.version,
            REASON_PROMPT_INFO.name: REASON_PROMPT_INFO.version,
        },
        "input_summary": {
            "top_tags": [
                {
                    "tag_code": tag.tag_code,
                    "score": tag.score,
                }
                for tag in rerank_input.user_profile.top_tags
            ],
            "candidate_ids": [
                candidate.game_id
                for candidate in rerank_input.candidates
            ],
        },
        "rerank": {
            "selected_top_3_game_ids": rerank_output.selected_top_3_game_ids,
            "latency_ms": rerank_latency_ms,
        },
        "reasons": {
            "top_3_reasons": reasons,
            "latency_ms": reasons_latency_ms,
        },
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a minimal LLM eval set for GRS.")
    parser.add_argument(
        "--case",
        choices=sorted(EVAL_CASES.keys()),
        help="Run one eval case. If omitted, all cases are run.",
    )
    parser.add_argument(
        "--output",
        default="app/llm/evals/latest_results.json",
        help="Path to write JSON results.",
    )
    args = parser.parse_args()

    selected_cases = (
        {args.case: EVAL_CASES[args.case]}
        if args.case
        else EVAL_CASES
    )

    results = [
        _run_case(case_name, rerank_input)
        for case_name, rerank_input in selected_cases.items()
    ]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"Wrote eval results to {output_path}")


if __name__ == "__main__":
    main()

