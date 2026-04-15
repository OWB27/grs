import { useTranslation } from "react-i18next";
import PanelCard from "../ui/PanelCard";

const pipelineSteps = [
  {
    id: 1,
    labelKey: "pipeline.step.survey",
    icon: "document",
    isActive: false,
  },
  {
    id: 2,
    labelKey: "pipeline.step.tagWeighting",
    icon: "tag",
    isActive: false,
  },
  {
    id: 3,
    labelKey: "pipeline.step.retrieval",
    icon: "database",
    isActive: false,
  },
  { id: 4, labelKey: "pipeline.step.results", icon: "badge", isActive: true },
];

function PipelineIcon({ type, active = false }) {
  const iconClass = active ? "text-cyan-300" : "text-cyan-400/90";
  const strokeWidth = 1.7;

  if (type === "document") {
    return (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        className={`h-6 w-6 ${iconClass}`}
        stroke="currentColor"
        strokeWidth={strokeWidth}
      >
        <path d="M7 3.75h6.5L18.25 8.5V19A1.25 1.25 0 0 1 17 20.25H7A1.25 1.25 0 0 1 5.75 19V5A1.25 1.25 0 0 1 7 3.75Z" />
        <path d="M13 3.75V8.5h4.75" />
        <path d="M8.5 12h7" />
        <path d="M8.5 15.5h7" />
      </svg>
    );
  }

  if (type === "tag") {
    return (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        className={`h-6 w-6 ${iconClass}`}
        stroke="currentColor"
        strokeWidth={strokeWidth}
      >
        <path d="M10 4.75H6.75A2 2 0 0 0 4.75 6.75V10a2 2 0 0 0 .59 1.41l7.25 7.25a2 2 0 0 0 2.82 0l3.25-3.25a2 2 0 0 0 0-2.82L11.41 5.34A2 2 0 0 0 10 4.75Z" />
        <circle cx="8.25" cy="8.25" r="1.1" fill="currentColor" stroke="none" />
      </svg>
    );
  }

  if (type === "database") {
    return (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        className={`h-6 w-6 ${iconClass}`}
        stroke="currentColor"
        strokeWidth={strokeWidth}
      >
        <ellipse cx="12" cy="6.25" rx="6.25" ry="2.75" />
        <path d="M5.75 6.25V11c0 1.52 2.8 2.75 6.25 2.75S18.25 12.52 18.25 11V6.25" />
        <path d="M5.75 11v4.75c0 1.52 2.8 2.75 6.25 2.75s6.25-1.23 6.25-2.75V11" />
      </svg>
    );
  }

  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      className={`h-6 w-6 ${iconClass}`}
      stroke="currentColor"
      strokeWidth={strokeWidth}
    >
      <path d="M12 4.75 14.06 6.2l2.48-.17 1.1 2.22 2.22 1.1-.17 2.48L21.25 14l-1.45 2.06.17 2.48-2.22 1.1-1.1 2.22-2.48-.17L12 23.25l-2.06-1.45-2.48.17-1.1-2.22-2.22-1.1.17-2.48L2.75 14l1.45-2.06-.17-2.48 2.22-1.1 1.1-2.22 2.48.17L12 4.75Z" />
      <path d="m9.25 12.25 1.75 1.75 3.75-4" />
    </svg>
  );
}

function PipelineStep({ step, showArrow = true, t }) {
  return (
    <>
      <div className="flex flex-col items-center">
        <div
          className={`flex h-14 w-14 items-center justify-center rounded-2xl border transition md:h-16 md:w-16 ${
            step.isActive
              ? "border-cyan-400/25 bg-cyan-400/[0.08]"
              : "border-white/8 bg-white/[0.02]"
          }`}
        >
          <PipelineIcon type={step.icon} active={step.isActive} />
        </div>

        <div className="mt-3 text-center">
          <div className="text-sm font-medium tracking-tight text-slate-200 md:text-[15px]">
            {t(step.labelKey)}
          </div>
        </div>
      </div>

      {showArrow ? (
        <div className="hidden items-center justify-center md:flex">
          <div className="flex items-center gap-2 text-cyan-400/100">
            <div className="h-px w-15 bg-cyan-400/60" />
            <svg
              viewBox="0 0 24 24"
              fill="none"
              className="h-4 w-4"
              stroke="currentColor"
              strokeWidth="1.8"
            >
              <path d="M5 12h13" />
              <path d="m13 6 6 6-6 6" />
            </svg>
          </div>
        </div>
      ) : null}
    </>
  );
}

export default function PipelinePanel() {
  const { t } = useTranslation();
  return (
    <PanelCard className="mx-auto max-w-4xl rounded-[24px] border-white/6 bg-white/[0.02] px-6 py-7 md:px-10 md:py-8">
      <div className="mb-7 text-center">
        <p className="font-mono text-xs tracking-wide text-slate-500 md:text-sm">
          // {t("pipeline.title")}
        </p>
      </div>

      <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-center md:gap-8 lg:gap-10">
        {pipelineSteps.map((step, index) => (
          <PipelineStep
            key={step.id}
            step={step}
            showArrow={index !== pipelineSteps.length - 1}
            t={t}
          />
        ))}
      </div>
    </PanelCard>
  );
}
