from app.schemas.llm_rerank import (
    LLMCandidateItem,
    LLMCandidateMatchedTag,
    LLMRerankInput,
    LLMRerankTask,
    LLMUserProfile,
    LLMUserProfileTag,
)


def _profile_tag(
    code: str,
    zh: str,
    en: str,
    description_zh: str,
    description_en: str,
    score: int,
) -> LLMUserProfileTag:
    return LLMUserProfileTag(
        tag_code=code,
        tag_name_zh=zh,
        tag_name_en=en,
        tag_description_zh=description_zh,
        tag_description_en=description_en,
        score=score,
    )


def _matched_tag(
    code: str,
    zh: str,
    en: str,
    description_zh: str,
    description_en: str,
    contribution: int,
) -> LLMCandidateMatchedTag:
    return LLMCandidateMatchedTag(
        tag_code=code,
        tag_name_zh=zh,
        tag_name_en=en,
        tag_description_zh=description_zh,
        tag_description_en=description_en,
        contribution=contribution,
    )


def _candidate(
    game_id: int,
    name_zh: str,
    name_en: str,
    rule_score: float,
    matched_tags: list[LLMCandidateMatchedTag],
) -> LLMCandidateItem:
    return LLMCandidateItem(
        game_id=game_id,
        name_zh=name_zh,
        name_en=name_en,
        rule_score=rule_score,
        matched_tags=matched_tags,
    )


STORY_IMMERSION_CASE = LLMRerankInput(
    task=LLMRerankTask(candidate_limit=6, select_count=3),
    user_profile=LLMUserProfile(
        top_tags=[
            _profile_tag(
                "story_rich",
                "剧情丰富",
                "Story Rich",
                "重视角色、叙事和沉浸式剧情体验。",
                "Focuses on characters, narrative, and immersive story experiences.",
                9,
            ),
            _profile_tag(
                "exploration",
                "自由探索",
                "Exploration",
                "喜欢开放区域、发现秘密和自主探索。",
                "Enjoys open areas, discovery, secrets, and self-directed exploration.",
                7,
            ),
            _profile_tag(
                "choices_matter",
                "选择影响",
                "Choices Matter",
                "希望选择能影响剧情、角色关系或结局。",
                "Wants choices to affect story, relationships, or endings.",
                6,
            ),
        ]
    ),
    candidates=[
        _candidate(
            1,
            "巫师 3：狂猎",
            "The Witcher 3: Wild Hunt",
            94.0,
            [
                _matched_tag("story_rich", "剧情丰富", "Story Rich", "重视角色、叙事和沉浸式剧情体验。", "Focuses on characters, narrative, and immersive story experiences.", 9),
                _matched_tag("exploration", "自由探索", "Exploration", "喜欢开放区域、发现秘密和自主探索。", "Enjoys open areas, discovery, secrets, and self-directed exploration.", 7),
                _matched_tag("choices_matter", "选择影响", "Choices Matter", "希望选择能影响剧情、角色关系或结局。", "Wants choices to affect story, relationships, or endings.", 6),
            ],
        ),
        _candidate(
            2,
            "极乐迪斯科",
            "Disco Elysium",
            91.0,
            [
                _matched_tag("story_rich", "剧情丰富", "Story Rich", "重视角色、叙事和沉浸式剧情体验。", "Focuses on characters, narrative, and immersive story experiences.", 9),
                _matched_tag("choices_matter", "选择影响", "Choices Matter", "希望选择能影响剧情、角色关系或结局。", "Wants choices to affect story, relationships, or endings.", 8),
            ],
        ),
        _candidate(
            3,
            "荒野大镖客：救赎 2",
            "Red Dead Redemption 2",
            88.0,
            [
                _matched_tag("story_rich", "剧情丰富", "Story Rich", "重视角色、叙事和沉浸式剧情体验。", "Focuses on characters, narrative, and immersive story experiences.", 8),
                _matched_tag("exploration", "自由探索", "Exploration", "喜欢开放区域、发现秘密和自主探索。", "Enjoys open areas, discovery, secrets, and self-directed exploration.", 8),
            ],
        ),
        _candidate(
            4,
            "哈迪斯",
            "Hades",
            78.0,
            [
                _matched_tag("combat", "战斗驱动", "Combat", "偏好高频战斗、操作挑战和动作反馈。", "Prefers frequent combat, mechanical challenge, and action feedback.", 8),
                _matched_tag("story_rich", "剧情丰富", "Story Rich", "重视角色、叙事和沉浸式剧情体验。", "Focuses on characters, narrative, and immersive story experiences.", 5),
            ],
        ),
        _candidate(
            5,
            "星露谷物语",
            "Stardew Valley",
            72.0,
            [
                _matched_tag("cozy", "轻松治愈", "Cozy", "偏好低压力、温暖和放松的体验。", "Prefers low-pressure, warm, and relaxing experiences.", 8),
                _matched_tag("exploration", "自由探索", "Exploration", "喜欢开放区域、发现秘密和自主探索。", "Enjoys open areas, discovery, secrets, and self-directed exploration.", 4),
            ],
        ),
        _candidate(
            6,
            "文明 VI",
            "Sid Meier's Civilization VI",
            69.0,
            [
                _matched_tag("strategy", "策略规划", "Strategy", "喜欢长期规划、资源管理和战术选择。", "Enjoys long-term planning, resource management, and tactical choices.", 9),
            ],
        ),
    ],
)


FAST_COMBAT_CASE = LLMRerankInput(
    task=LLMRerankTask(candidate_limit=6, select_count=3),
    user_profile=LLMUserProfile(
        top_tags=[
            _profile_tag("combat", "战斗驱动", "Combat", "偏好高频战斗、操作挑战和动作反馈。", "Prefers frequent combat, mechanical challenge, and action feedback.", 9),
            _profile_tag("fast_paced", "快节奏", "Fast Paced", "喜欢快速反应、紧张节奏和持续行动。", "Enjoys quick reactions, intense pacing, and constant action.", 8),
            _profile_tag("replayable", "高重玩性", "Replayable", "希望每局体验有变化，适合反复游玩。", "Wants varied runs and strong replay value.", 6),
        ]
    ),
    candidates=[
        _candidate(
            11,
            "哈迪斯",
            "Hades",
            95.0,
            [
                _matched_tag("combat", "战斗驱动", "Combat", "偏好高频战斗、操作挑战和动作反馈。", "Prefers frequent combat, mechanical challenge, and action feedback.", 9),
                _matched_tag("fast_paced", "快节奏", "Fast Paced", "喜欢快速反应、紧张节奏和持续行动。", "Enjoys quick reactions, intense pacing, and constant action.", 8),
                _matched_tag("replayable", "高重玩性", "Replayable", "希望每局体验有变化，适合反复游玩。", "Wants varied runs and strong replay value.", 7),
            ],
        ),
        _candidate(
            12,
            "毁灭战士：永恒",
            "DOOM Eternal",
            92.0,
            [
                _matched_tag("combat", "战斗驱动", "Combat", "偏好高频战斗、操作挑战和动作反馈。", "Prefers frequent combat, mechanical challenge, and action feedback.", 10),
                _matched_tag("fast_paced", "快节奏", "Fast Paced", "喜欢快速反应、紧张节奏和持续行动。", "Enjoys quick reactions, intense pacing, and constant action.", 9),
            ],
        ),
        _candidate(
            13,
            "死亡细胞",
            "Dead Cells",
            88.0,
            [
                _matched_tag("combat", "战斗驱动", "Combat", "偏好高频战斗、操作挑战和动作反馈。", "Prefers frequent combat, mechanical challenge, and action feedback.", 8),
                _matched_tag("replayable", "高重玩性", "Replayable", "希望每局体验有变化，适合反复游玩。", "Wants varied runs and strong replay value.", 9),
            ],
        ),
        _candidate(
            14,
            "空洞骑士",
            "Hollow Knight",
            82.0,
            [
                _matched_tag("combat", "战斗驱动", "Combat", "偏好高频战斗、操作挑战和动作反馈。", "Prefers frequent combat, mechanical challenge, and action feedback.", 7),
                _matched_tag("exploration", "自由探索", "Exploration", "喜欢开放区域、发现秘密和自主探索。", "Enjoys open areas, discovery, secrets, and self-directed exploration.", 7),
            ],
        ),
        _candidate(
            15,
            "极乐迪斯科",
            "Disco Elysium",
            64.0,
            [
                _matched_tag("story_rich", "剧情丰富", "Story Rich", "重视角色、叙事和沉浸式剧情体验。", "Focuses on characters, narrative, and immersive story experiences.", 9),
            ],
        ),
        _candidate(
            16,
            "城市：天际线",
            "Cities: Skylines",
            58.0,
            [
                _matched_tag("strategy", "策略规划", "Strategy", "喜欢长期规划、资源管理和战术选择。", "Enjoys long-term planning, resource management, and tactical choices.", 8),
            ],
        ),
    ],
)


EVAL_CASES = {
    "story_immersion": STORY_IMMERSION_CASE,
    "fast_combat": FAST_COMBAT_CASE,
}
