import { useTranslation } from "react-i18next";

export default function ProgressBar({ current, total }) {
  const { t } = useTranslation();

  return (
    <div className="flex flex-col items-center">
      <div className="mb-5 flex items-baseline gap-2 font-ui">
        <span className="text-[15px] font-medium text-cyan-400 md:text-lg">
          {current}
        </span>
        <span className="text-[15px] text-slate-500 md:text-lg">/</span>
        <span className="text-[15px] font-medium text-slate-300 md:text-lg">
          {total}
        </span>
        <span className="ml-2 text-[14px] text-slate-500 md:text-base">
          {t("quiz.progressUnit")}
        </span>
      </div>

      <div className="flex items-center gap-3">
        {Array.from({ length: total }).map((_, index) => {
          const step = index + 1;
          const isCurrent = step === current;
          const isDone = step < current;

          return (
            <div
              key={step}
              className={[
                "rounded-full transition-all duration-300",
                isCurrent
                  ? "h-5 w-5 bg-cyan-400 shadow-[0_0_18px_rgba(34,211,238,0.85),0_0_36px_rgba(34,211,238,0.35)]"
                  : isDone
                    ? "h-4 w-4 bg-cyan-400/65"
                    : "h-4 w-4 bg-white/[0.08]",
              ].join(" ")}
            />
          );
        })}
      </div>
    </div>
  );
}
