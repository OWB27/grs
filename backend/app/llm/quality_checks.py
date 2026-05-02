from app.schemas.llm_rerank import LLMReasonsOutput, LLMRerankInput, LLMRerankOutput


def contains_cjk(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def looks_complete_sentence(text: str) -> bool:
    stripped = text.strip()
    return stripped.endswith((".", "!", "?"))


def internal_tag_codes(tag_codes: list[str]) -> list[str]:
    return [
        tag_code
        for tag_code in tag_codes
        if "_" in tag_code
    ]


def contains_any(text: str, values: list[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def get_llm_output_hard_failures(
    rerank_input: LLMRerankInput,
    rerank_output: LLMRerankOutput,
    reasons_output: LLMReasonsOutput,
) -> list[str]:
    failures: list[str] = []
    candidate_ids = [candidate.game_id for candidate in rerank_input.candidates]
    selected_ids = rerank_output.selected_top_3_game_ids

    if len(selected_ids) != 3:
        failures.append("selected_top_3_game_ids_count_is_not_3")

    if len(set(selected_ids)) != len(selected_ids):
        failures.append("selected_top_3_game_ids_contains_duplicates")

    if not set(selected_ids).issubset(set(candidate_ids)):
        failures.append("selected_top_3_game_ids_contains_unknown_candidate")

    reason_ids = [item.game_id for item in reasons_output.top_3_reasons]
    if reason_ids != selected_ids:
        failures.append("reason_ids_do_not_match_selected_order")

    for item in reasons_output.top_3_reasons:
        if not item.reason.zh:
            failures.append(f"empty_zh_reason_for_game_{item.game_id}")
        if not item.reason.en:
            failures.append(f"empty_en_reason_for_game_{item.game_id}")

    return failures


def get_llm_output_soft_warnings(
    rerank_input: LLMRerankInput,
    reasons_output: LLMReasonsOutput,
) -> list[str]:
    warnings: list[str] = []
    top_tag_codes = internal_tag_codes(
        [tag.tag_code for tag in rerank_input.user_profile.top_tags]
    )

    for item in reasons_output.top_3_reasons:
        zh_reason = item.reason.zh
        en_reason = item.reason.en

        if contains_cjk(en_reason):
            warnings.append(f"en_reason_contains_chinese_for_game_{item.game_id}")

        if en_reason and not looks_complete_sentence(en_reason):
            warnings.append(f"en_reason_may_be_incomplete_for_game_{item.game_id}")

        if contains_any(zh_reason, top_tag_codes) or contains_any(en_reason, top_tag_codes):
            warnings.append(f"reason_exposes_tag_code_for_game_{item.game_id}")

    return warnings
