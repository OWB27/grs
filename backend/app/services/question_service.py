def get_questions_by_lang(lang: str) -> list[dict]:
    use_zh = lang == "zh"

    return [
        {
            "id": 1,
            "code": "preferred_experience",
            "title": "你更喜欢哪种游戏体验？" if use_zh else "What kind of experience do you prefer?",
            "sort_order": 1,
            "options": [
                {
                    "id": 11,
                    "code": "story_immersion",
                    "text": "沉浸剧情" if use_zh else "Immersive story",
                    "sort_order": 1,
                },
                {
                    "id": 12,
                    "code": "free_exploration",
                    "text": "自由探索" if use_zh else "Free exploration",
                    "sort_order": 2,
                },
                {
                    "id": 13,
                    "code": "competitive_challenge",
                    "text": "挑战与对抗" if use_zh else "Challenge and competition",
                    "sort_order": 3,
                },
            ],
        },
        {
            "id": 2,
            "code": "game_pace",
            "title": "你更喜欢什么节奏？" if use_zh else "What pace do you prefer?",
            "sort_order": 2,
            "options": [
                {
                    "id": 21,
                    "code": "slow_relaxed",
                    "text": "慢节奏、轻松一些" if use_zh else "Slow and relaxed",
                    "sort_order": 1,
                },
                {
                    "id": 22,
                    "code": "balanced_pace",
                    "text": "节奏均衡" if use_zh else "Balanced pace",
                    "sort_order": 2,
                },
                {
                    "id": 23,
                    "code": "fast_intense",
                    "text": "快节奏、刺激一些" if use_zh else "Fast and intense",
                    "sort_order": 3,
                },
            ],
        },
    ]