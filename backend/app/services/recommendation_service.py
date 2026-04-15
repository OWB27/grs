def build_mock_recommendations(answers: list[dict] | list, lang: str) -> list[dict]:
    use_zh = lang == "zh"

    # 先做一个极简假逻辑：
    # 只要第一个问题选了 11，就返回剧情向结果，否则返回动作向结果
    first_answer_option_id = None

    for answer in answers:
        question_id = answer.question_id if hasattr(answer, "question_id") else answer["question_id"]
        option_id = answer.option_id if hasattr(answer, "option_id") else answer["option_id"]

        if question_id == 1:
            first_answer_option_id = option_id
            break

    if first_answer_option_id == 11:
        return [
            {
                "game_id": 101,
                "name_zh": "巫师 3：狂猎" if use_zh else "The Witcher 3: Wild Hunt",
                "name_en": "The Witcher 3: Wild Hunt",
                "steam_url": "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/",
                "reason": "你偏好剧情沉浸和探索，因此这款游戏更适合你。"
                if use_zh
                else "You prefer immersive storytelling and exploration, so this game fits you better.",
            },
            {
                "game_id": 102,
                "name_zh": "极乐迪斯科" if use_zh else "Disco Elysium",
                "name_en": "Disco Elysium",
                "steam_url": "https://store.steampowered.com/app/632470/Disco_Elysium__The_Final_Cut/",
                "reason": "你对叙事和角色塑造更敏感，这类作品匹配度较高。"
                if use_zh
                else "Your answers suggest a stronger preference for narrative and character-driven games.",
            },
        ]

    return [
        {
            "game_id": 201,
            "name_zh": "黑帝斯" if use_zh else "Hades",
            "name_en": "Hades",
            "steam_url": "https://store.steampowered.com/app/1145360/Hades/",
            "reason": "你的回答更偏向节奏紧凑和高反馈的玩法。"
            if use_zh
            else "Your answers lean toward fast pacing and strong gameplay feedback.",
        },
        {
            "game_id": 202,
            "name_zh": "怪物猎人：世界" if use_zh else "Monster Hunter: World",
            "name_en": "Monster Hunter: World",
            "steam_url": "https://store.steampowered.com/app/582010/Monster_Hunter_World/",
            "reason": "你更能接受挑战与成长循环，这类游戏会更适合你。"
            if use_zh
            else "You seem more comfortable with challenge and progression loops, which suits this kind of game.",
        },
    ]