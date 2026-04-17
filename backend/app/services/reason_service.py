from copy import deepcopy


def _fallback_reason() -> dict[str, str]:
    return {
        "zh": "这款游戏与你的整体偏好画像较为匹配，因此进入了本次推荐结果。",
        "en": "This game matches your overall preference profile well, so it appears in the recommendation results.",
    }


def _build_reason_from_tags(matched_tags: list[dict]) -> dict[str, str]:
    if not matched_tags:
        return _fallback_reason()

    top_tags = matched_tags[:2]
    tag_codes = [item["tagCode"] for item in top_tags]
    zh_names = [item["tagNameZh"] for item in top_tags]
    en_names = [item["tagNameEn"] for item in top_tags]

    if len(tag_codes) == 1:
        zh_text = zh_names[0]
        en_text = en_names[0]
    else:
        zh_text = f"{zh_names[0]}、{zh_names[1]}"
        en_text = f"{en_names[0]} and {en_names[1]}"

    return {
        "zh": f"因为你的回答在 {zh_text} 这些维度上表现更明显，而这款游戏在这些标签上的匹配度较高。",
        "en": f"Your answers show a stronger preference for {en_text}, and this game matches well on those dimensions.",
    }


def generate_reasons(top_candidates: list[dict], user_profile: dict[str, int]) -> list[dict]:
    reasoned_candidates: list[dict] = []

    for candidate in top_candidates:
        candidate_copy = deepcopy(candidate)
        matched_tags = candidate_copy.get("matchedTags", [])
        candidate_copy["reason"] = _build_reason_from_tags(matched_tags)
        reasoned_candidates.append(candidate_copy)

    return reasoned_candidates