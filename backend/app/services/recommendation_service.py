def build_mock_recommendations(answers: list, lang: str) -> list[dict]:
    first_answer_option_id = None

    for answer in answers:
        option_id = answer.optionId if hasattr(answer, "optionId") else answer["optionId"]
        question_id = answer.questionId if hasattr(answer, "questionId") else answer["questionId"]

        if question_id == 1:
            first_answer_option_id = option_id
            break

    if first_answer_option_id == 11:
        return [
            {
                "gameId": 101,
                "name": {
                    "zh": "巫师 3：狂猎",
                    "en": "The Witcher 3: Wild Hunt",
                },
                "steamUrl": "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/",
                "reason": {
                    "zh": "你偏好剧情沉浸、角色成长和世界探索，因此这款作品很适合作为你的第一推荐。",
                    "en": "You seem to like immersive storytelling, character growth, and exploration, so this is a strong first pick.",
                },
            },
            {
                "gameId": 102,
                "name": {
                    "zh": "极乐迪斯科",
                    "en": "Disco Elysium",
                },
                "steamUrl": "https://store.steampowered.com/app/632470/Disco_Elysium__The_Final_Cut/",
                "reason": {
                    "zh": "你对叙事和角色塑造的偏好比较明显，这类文本与剧情驱动作品会更适合你。",
                    "en": "Your answers show a strong preference for narrative and character-driven experiences.",
                },
            },
        ]

    return [
        {
            "gameId": 201,
            "name": {
                "zh": "黑帝斯",
                "en": "Hades",
            },
            "steamUrl": "https://store.steampowered.com/app/1145360/Hades/",
            "reason": {
                "zh": "你的回答更偏向节奏紧凑和高反馈的玩法。",
                "en": "Your answers lean toward fast pacing and strong gameplay feedback.",
            },
        },
        {
            "gameId": 202,
            "name": {
                "zh": "怪物猎人：世界",
                "en": "Monster Hunter: World",
            },
            "steamUrl": "https://store.steampowered.com/app/582010/Monster_Hunter_World/",
            "reason": {
                "zh": "你更能接受挑战与成长循环，这类游戏会更适合你。",
                "en": "You seem more comfortable with challenge and progression loops, which suits this kind of game.",
            },
        },
    ]