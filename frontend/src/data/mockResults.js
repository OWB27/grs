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
