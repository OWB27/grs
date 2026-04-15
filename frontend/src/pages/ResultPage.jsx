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

export default function ResultPage() {
  const { i18n, t } = useTranslation();
  const location = useLocation();
  const RecommendationComponent =
    import.meta.env.VITE_SHOW_RESULT_DEBUG === "true"
      ? RecommendationDebugCard
      : RecommendationCard;

  const recommendations = location.state?.recommendations ?? [];
  const lang = i18n.language;

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
            <div className="grid gap-6 lg:grid-cols-3">
              {recommendations.map((item) => (
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
