import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router";

import AppShell from "../components/layout/AppShell";
import PageSection from "../components/layout/PageSection";
import TopNav from "../components/common/TopNav";
import PageIntro from "../components/common/PageIntro";
import EmptyStatePanel from "../components/common/EmptyStatePanel";
import SecondaryButton from "../components/ui/SecondaryButton";
import ActionRow from "../components/ui/ActionRow";
import RecommendationCard from "../components/result/RecommendationCard";
import RecommendationDebugCard from "../components/result/RecommendationDebugCard";

const BATCH_SIZE = 3;

export default function ResultPage() {
  const { i18n, t } = useTranslation();
  const location = useLocation();

  const RecommendationComponent =
    import.meta.env.VITE_SHOW_RESULT_DEBUG === "true"
      ? RecommendationDebugCard
      : RecommendationCard;

  const recommendations = location.state?.recommendations ?? [];
  const lang = i18n.language;

  const [batchStart, setBatchStart] = useState(0);

  const visibleRecommendations = recommendations.slice(
    batchStart,
    batchStart + BATCH_SIZE
  );

  function handleNextBatch() {
    const nextStart = batchStart + BATCH_SIZE;

    if (nextStart >= recommendations.length) {
      setBatchStart(0);
      return;
    }

    setBatchStart(nextStart);
  }

  const totalBatches =
    recommendations.length > 0
      ? Math.ceil(recommendations.length / BATCH_SIZE)
      : 0;

  const currentBatch =
    recommendations.length > 0 ? Math.floor(batchStart / BATCH_SIZE) + 1 : 0;

  return (
    <AppShell>
      <TopNav />

      <PageSection width="xl">
        <PageIntro
          code={t("result.pageCode")}
          title={t("result.title")}
          subtitle={t("result.subtitle")}
          centered
          className="mb-8"
        />

        {recommendations.length === 0 ? (
          <EmptyStatePanel
            code={t("result.emptyCode")}
            message={t("result.emptyText")}
            actions={
              <ActionRow>
                <SecondaryButton to="/">{t("backHome")}</SecondaryButton>
                <SecondaryButton to="/quiz">{t("retry")}</SecondaryButton>
              </ActionRow>
            }
          />
        ) : (
          <>
            <div className="mb-6 flex items-center justify-between gap-4">
              <div className="font-mono text-xs text-slate-400">
                {currentBatch}/{totalBatches}
              </div>

              <ActionRow>
                <SecondaryButton onClick={handleNextBatch}>
                  {t("nextBatch")}
                </SecondaryButton>
              </ActionRow>
            </div>

            <div className="grid gap-6 lg:grid-cols-3">
              {visibleRecommendations.map((item) => (
                <RecommendationComponent
                  key={item.gameId}
                  item={item}
                  lang={lang}
                />
              ))}
            </div>

            <ActionRow className="mt-10">
              <SecondaryButton to="/quiz">{t("retry")}</SecondaryButton>
              <SecondaryButton to="/">{t("backHome")}</SecondaryButton>
            </ActionRow>
          </>
        )}
      </PageSection>
    </AppShell>
  );
}