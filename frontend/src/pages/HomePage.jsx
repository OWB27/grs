import { useEffect } from "react";
import { useTranslation } from "react-i18next";

import AppShell from "../components/layout/AppShell";
import PageSection from "../components/layout/PageSection";
import TopNav from "../components/common/TopNav";
import PrimaryButton from "../components/ui/PrimaryButton";
import SecondaryButton from "../components/ui/SecondaryButton";
import PipelinePanel from "../components/home/PipelinePanel";
import { prefetchQuestions } from "../lib/api";

export default function HomePage() {
  const { t } = useTranslation();

  useEffect(() => {
    prefetchQuestions();
  }, []);

  return (
    <AppShell>
      <TopNav />

      <PageSection width="md" centered>
        <div className="inline-flex items-center gap-2.5 rounded-full border border-cyan-400/18 bg-cyan-400/[0.06] px-4 py-2 font-mono text-xs text-cyan-300">
          <span className="h-2 w-2 rounded-full bg-cyan-300" />
          <span>{t("home.engineBadge")}</span>
        </div>

        <h1 className="mt-8 text-4xl font-bold leading-[0.98] tracking-tight text-white md:text-6xl">
          <span className="block">{t("home.heroTitleLine1")}</span>
          <span className="mt-1.5 block text-cyan-400">
            {t("home.heroTitleLine2")}
          </span>
        </h1>

        <p className="mx-auto mt-6 max-w-xl text-base leading-8 text-slate-400 md:text-lg">
          {t("home.heroSubtitle")}
        </p>

        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <PrimaryButton to="/quiz">
            {t("startQuiz")}
            <svg
              viewBox="0 0 24 24"
              fill="none"
              className="h-4.5 w-4.5"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M5 12h13" />
              <path d="m13 6 6 6-6 6" />
            </svg>
          </PrimaryButton>

          <SecondaryButton>
            {t("home.methodology")}
          </SecondaryButton>
        </div>
      </PageSection>

      <PageSection className="mt-14 md:mt-16">
        <PipelinePanel />
      </PageSection>
    </AppShell>
  );
}