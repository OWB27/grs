import argparse
import json
import time
from pathlib import Path
from typing import Any

from app.llm.reason_client import call_llm_reason_generation
from app.llm.rerank_client import call_llm_rerank
from app.llm.evals.sample_cases import EVAL_CASES
from app.llm.prompts.registry import REASON_PROMPT_INFO, RERANK_PROMPT_INFO
from app.llm.quality_checks import get_llm_output_hard_failures, get_llm_output_soft_warnings
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
    hard_failures = get_llm_output_hard_failures(
        rerank_input,
        rerank_output,
        reasons_output,
    )
    soft_warnings = get_llm_output_soft_warnings(
        rerank_input,
        reasons_output,
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
        "hard_failures": hard_failures,
        "soft_warnings": soft_warnings,
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

