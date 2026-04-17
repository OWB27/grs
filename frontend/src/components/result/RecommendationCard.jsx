import { useTranslation } from "react-i18next";

import ActionRow from "../ui/ActionRow";
import SteamButton from "../ui/SteamButton";

function CoverImage({ src, alt }) {
  if (!src) {
    return (
      <div className="relative overflow-hidden rounded-t-[26px] border-b border-white/8 bg-[linear-gradient(135deg,rgba(17,54,66,0.75),rgba(15,24,39,0.9),rgba(17,54,66,0.72))]">
        <div className="aspect-[16/10] w-full" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.12),transparent_35%)]" />
        <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-[#0b1220] to-transparent" />
      </div>
    );
  }

  return (
    <div className="relative overflow-hidden rounded-t-[26px] border-b border-white/8 bg-black">
      <img
        src={src}
        alt={alt}
        className="aspect-[16/10] w-full object-cover"
        loading="lazy"
      />
      <div className="absolute inset-0 bg-[linear-gradient(to_top,rgba(11,18,32,0.72),rgba(11,18,32,0.08),transparent)]" />
      <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-[#0b1220] to-transparent" />
    </div>
  );
}

export default function RecommendationCard({ item, lang, actions, children }) {
  const { t } = useTranslation();

  const displayName = item?.name?.[lang] ?? item?.name?.en ?? "Unknown Game";
  const displayReason = item?.reason?.[lang] ?? item?.reason?.en ?? "";
  const coverImageUrl = item?.coverImageUrl ?? null;
  const cardActions = actions ?? <SteamButton href={item?.steamUrl} />;

  return (
    <article className="overflow-hidden rounded-[26px] border border-cyan-400/20 bg-[#0b1220]/95 shadow-[0_8px_40px_rgba(0,0,0,0.28)]">
      <CoverImage src={coverImageUrl} alt={displayName} />

      <div className="px-5 py-5 md:px-6 md:py-6">
        <div>
          <h3 className="text-2xl font-semibold tracking-tight text-white">
            {displayName}
          </h3>
        </div>

        <div className="mt-6 rounded-2xl border border-white/8 bg-white/[0.02] p-4">
          <div className="mb-3 text-xl font-semibold tracking-tight text-cyan-400">
            {t("result.whyThis")}
          </div>

          <p className="text-base leading-8 text-slate-400">
            {displayReason}
          </p>
        </div>

        <ActionRow align="start" className="mt-6">
          {cardActions}
        </ActionRow>
      </div>

      {children}
    </article>
  );
}