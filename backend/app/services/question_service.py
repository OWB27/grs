def get_questions() -> list[dict]:
    return [
        {
            "id": 1,
            "code": "preferred_experience",
            "sortOrder": 1,
            "title": {
                "zh": "你更喜欢哪种游戏体验？",
                "en": "What kind of game experience do you prefer?",
            },
            "options": [
                {
                    "id": 11,
                    "code": "story_immersion",
                    "sortOrder": 1,
                    "text": {
                        "zh": "沉浸剧情",
                        "en": "Immersive story",
                    },
                },
                {
                    "id": 12,
                    "code": "free_exploration",
                    "sortOrder": 2,
                    "text": {
                        "zh": "自由探索",
                        "en": "Free exploration",
                    },
                },
                {
                    "id": 13,
                    "code": "competitive_challenge",
                    "sortOrder": 3,
                    "text": {
                        "zh": "挑战与对抗",
                        "en": "Challenge and competition",
                    },
                },
            ],
        },
        {
            "id": 2,
            "code": "game_pace",
            "sortOrder": 2,
            "title": {
                "zh": "你更喜欢什么节奏？",
                "en": "What pace do you prefer?",
            },
            "options": [
                {
                    "id": 21,
                    "code": "slow_relaxed",
                    "sortOrder": 1,
                    "text": {
                        "zh": "慢节奏、轻松一些",
                        "en": "Slow and relaxed",
                    },
                },
                {
                    "id": 22,
                    "code": "balanced_pace",
                    "sortOrder": 2,
                    "text": {
                        "zh": "节奏均衡",
                        "en": "Balanced pace",
                    },
                },
                {
                    "id": 23,
                    "code": "fast_intense",
                    "sortOrder": 3,
                    "text": {
                        "zh": "快节奏、刺激一些",
                        "en": "Fast and intense",
                    },
                },
            ],
        },
    ]