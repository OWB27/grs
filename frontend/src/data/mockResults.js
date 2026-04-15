const resultGroups = {
  story: [
    {
      gameId: 101,
      name: {
        zh: "巫师 3：狂猎",
        en: "The Witcher 3: Wild Hunt",
      },
      steamUrl: "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/",
      reason: {
        zh: "你偏好剧情沉浸、角色成长和世界探索，因此这款作品很适合作为你的第一推荐。",
        en: "You seem to like immersive storytelling, character growth, and exploration, so this is a strong first pick.",
      },
    },
    {
      gameId: 102,
      name: {
        zh: "极乐迪斯科",
        en: "Disco Elysium",
      },
      steamUrl: "https://store.steampowered.com/app/632470/Disco_Elysium__The_Final_Cut/",
      reason: {
        zh: "你对叙事和角色塑造的偏好比较明显，这类文本与剧情驱动作品会更适合你。",
        en: "Your answers show a strong preference for narrative and character-driven experiences.",
      },
    },
    {
      gameId: 103,
      name: {
        zh: "赛博朋克 2077",
        en: "Cyberpunk 2077",
      },
      steamUrl: "https://store.steampowered.com/app/1091500/Cyberpunk_2077/",
      reason: {
        zh: "如果你喜欢世界观完整、可探索内容丰富的游戏，这类开放叙事作品通常匹配度较高。",
        en: "If you enjoy rich world-building and explorable content, open narrative-heavy games usually fit well.",
      },
    },
  ],
  cozy: [
    {
      gameId: 201,
      name: {
        zh: "星露谷物语",
        en: "Stardew Valley",
      },
      steamUrl: "https://store.steampowered.com/app/413150/Stardew_Valley/",
      reason: {
        zh: "你的答案更偏向轻松、低压力和经营建造，因此这类治愈向游戏会更适合你。",
        en: "Your answers lean toward relaxed, low-pressure, and management-focused play, which makes cozy games a better fit.",
      },
    },
    {
      gameId: 202,
      name: {
        zh: "动物森友会（示意）",
        en: "Animal Crossing (placeholder)",
      },
      steamUrl: "https://www.nintendo.com/",
      reason: {
        zh: "你似乎更看重舒适体验和日常经营感，这类作品通常更容易长期游玩。",
        en: "You seem to value comfort and everyday progression, which usually matches this style well.",
      },
    },
    {
      gameId: 203,
      name: {
        zh: "蔚蓝海岸农场（示意）",
        en: "Cozy Farm by the Sea (placeholder)",
      },
      steamUrl: "https://store.steampowered.com/",
      reason: {
        zh: "建造、收集和缓慢推进的节奏和你的问卷选择比较一致。",
        en: "The building, collecting, and slower progression style aligns with your quiz answers.",
      },
    },
  ],
  action: [
    {
      gameId: 301,
      name: {
        zh: "黑帝斯",
        en: "Hades",
      },
      steamUrl: "https://store.steampowered.com/app/1145360/Hades/",
      reason: {
        zh: "你的选择更偏向紧凑节奏和战斗反馈，这类高重复可玩性的动作游戏比较适合你。",
        en: "Your answers point to faster pacing and satisfying combat feedback, which suits replayable action games.",
      },
    },
    {
      gameId: 302,
      name: {
        zh: "Apex Legends",
        en: "Apex Legends",
      },
      steamUrl: "https://store.steampowered.com/app/1172470/Apex_Legends/",
      reason: {
        zh: "如果你喜欢刺激、对抗和团队配合，这类竞技导向的游戏会更匹配。",
        en: "If you enjoy intensity, competition, and team play, competitive games are likely a better match.",
      },
    },
    {
      gameId: 303,
      name: {
        zh: "怪物猎人：世界",
        en: "Monster Hunter: World",
      },
      steamUrl: "https://store.steampowered.com/app/582010/Monster_Hunter_World/",
      reason: {
        zh: "你对挑战、成长和战斗循环的接受度较高，这类作品通常会更耐玩。",
        en: "You seem comfortable with challenge, progression, and combat loops, which makes this style a strong fit.",
      },
    },
  ],
};

const defaultRecommendationDebug = {
  score: 18.5,
  rankingMode: "rule_based",
  matchedTags: [
    { tagCode: "story_rich", weight: 5 },
    { tagCode: "open_world", weight: 4 },
  ],
};

export function getMockRecommendationDebug(item) {
  return {
    score: item.debug?.score ?? item.score ?? defaultRecommendationDebug.score,
    rankingMode:
      item.debug?.rankingMode ??
      item.rankingMode ??
      defaultRecommendationDebug.rankingMode,
    matchedTags:
      item.debug?.matchedTags ??
      item.matchedTags ??
      defaultRecommendationDebug.matchedTags,
  };
}

export function getMockRecommendations(answers) {
  const firstAnswer = answers[1];
  const secondAnswer = answers[2];
  const thirdAnswer = answers[3];
  const fourthAnswer = answers[4];

  if (firstAnswer === 11 || fourthAnswer === 41) {
    return resultGroups.story;
  }

  if (secondAnswer === 21 || thirdAnswer === 32 || fourthAnswer === 42) {
    return resultGroups.cozy;
  }

  return resultGroups.action;
}
