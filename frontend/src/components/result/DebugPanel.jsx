import { useTranslation } from "react-i18next";

export default function DebugPanel({ debug, gameId }) {
  const { t, i18n } = useTranslation();

  if (!debug) {
    return (
      <div className="border-t border-white/8 bg-white/[0.02] px-5 py-5">
        <div className="mb-4 flex items-center gap-3 font-mono">
          <span className="rounded-md bg-cyan-400/12 px-2.5 py-1 text-xs text-cyan-300">
            {t("debug.title")}
          </span>
          <span className="text-xs text-slate-400">{t("debug.analysis")}</span>
        </div>

        <div className="rounded-xl border border-white/6 bg-black/25 p-4 font-mono text-xs text-slate-400">
          {t("debug.noData")}
        </div>
      </div>
    );
  }

  return (
    <div className="border-t border-white/8 bg-white/[0.02] px-5 py-5">
      <div className="mb-4 flex items-center gap-3 font-mono">
        <span className="rounded-md bg-cyan-400/12 px-2.5 py-1 text-xs text-cyan-300">
          {t("debug.title")}
        </span>
        <span className="text-xs text-slate-400">{t("debug.analysis")}</span>
      </div>

      <div className="space-y-3">
        {debug.matchedTags.map((tag) => {
          const label =
            i18n.language === "zh"
              ? tag.tagNameZh || tag.tagCode
              : tag.tagNameEn || tag.tagCode;

          const percent = Math.min(
            Math.max(tag.contribution * 4, 20),
            100
          );

          return (
            <div
              key={tag.tagCode}
              className="grid grid-cols-[96px_1fr_52px] items-center gap-3"
            >
              <div className="font-mono text-xs text-slate-400">
                {label}:
              </div>

              <div className="h-2 rounded-full bg-white/[0.05]">
                <div
                  className="h-2 rounded-full bg-[#47d85a]"
                  style={{ width: `${percent}%` }}
                />
              </div>

              <div className="text-right font-mono text-xs text-[#47d85a]">
                +{tag.contribution}
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-5 overflow-x-auto rounded-xl border border-white/6 bg-black/25 p-4">
        <pre className="font-mono text-xs leading-6 text-slate-400">
{`{
  "game_id": ${gameId},
  "match_score": ${debug.score},
  "ranking_mode": "${debug.rankingMode}",
  "matched_tags": [
${debug.matchedTags
  .map(
    (tag) => `    {
      "tag_code": "${tag.tagCode}",
      "game_weight": ${tag.gameWeight},
      "user_weight": ${tag.userWeight},
      "contribution": ${tag.contribution}
    }`
  )
  .join(",\n")}
  ]
}`}
        </pre>
      </div>
    </div>
  );
}