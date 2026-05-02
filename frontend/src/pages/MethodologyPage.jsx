import { useTranslation } from "react-i18next";

import TopNav from "../components/common/TopNav";
import PageIntro from "../components/common/PageIntro";
import AppShell from "../components/layout/AppShell";
import PageSection from "../components/layout/PageSection";
import PanelCard from "../components/ui/PanelCard";
import PrimaryButton from "../components/ui/PrimaryButton";
import SecondaryButton from "../components/ui/SecondaryButton";

const stepKeys = [
  "methodology.step.profile",
  "methodology.step.matching",
  "methodology.step.rerank",
  "methodology.step.fallback",
];

const principleKeys = [
  "methodology.principle.transparent",
  "methodology.principle.bounded",
  "methodology.principle.stable",
];

export default function MethodologyPage() {
  const { t } = useTranslation();

  return (
    <AppShell>
      <TopNav />

      <PageSection width="lg">
        <PageIntro
          code={t("methodology.code")}
          title={t("methodology.title")}
          subtitle={t("methodology.subtitle")}
        />

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {stepKeys.map((key, index) => (
            <PanelCard key={key}>
              <div className="font-mono text-xs text-cyan-300">
                0{index + 1}
              </div>
              <p className="mt-3 text-sm leading-7 text-slate-300">
                {t(key)}
              </p>
            </PanelCard>
          ))}
        </div>

        <PanelCard className="mt-5">
          <p className="font-mono text-xs tracking-wide text-slate-500">
            // {t("methodology.principlesTitle")}
          </p>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            {principleKeys.map((key) => (
              <div
                key={key}
                className="rounded-2xl border border-white/8 bg-white/[0.02] px-4 py-4 text-sm leading-6 text-slate-300"
              >
                {t(key)}
              </div>
            ))}
          </div>
        </PanelCard>

        <div className="mt-8 flex flex-col gap-3 sm:flex-row">
          <PrimaryButton to="/quiz">{t("startQuiz")}</PrimaryButton>
          <SecondaryButton to="/">{t("backHome")}</SecondaryButton>
        </div>
      </PageSection>
    </AppShell>
  );
}
