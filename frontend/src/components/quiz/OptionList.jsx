export default function OptionList({
  options,
  selectedOptionId,
  onSelect,
  lang,
}) {
  return (
    <div className="space-y-4">
      {options.map((option) => {
        const isSelected = selectedOptionId === option.id;

        return (
          <button
            key={option.id}
            type="button"
            onClick={() => onSelect(option.id)}
            className={[
              "w-full rounded-2xl border px-6 py-6 text-left transition duration-200",
              "bg-[#101926]/85 backdrop-blur-sm",
              isSelected
                ? "border-cyan-400/30 bg-cyan-400/[0.06]"
                : "border-white/8 hover:border-white/14 hover:bg-white/[0.035]",
            ].join(" ")}
          >
            <div className="flex items-center gap-4">
              <div
                className={[
                  "h-5 w-5 shrink-0 rounded-full transition-all duration-200", // 加上 duration-200 让边框变粗的动画更平滑
                  isSelected
                    ? "border-[6px] border-cyan-400 bg-white shadow-[0_0_12px_rgba(34,211,238,0.35)]" // 6px 的边框会向内挤压，产生实心点的视觉效果
                    : "border-2 border-slate-500 bg-transparent",
                ].join(" ")}
              />

              <div className="text-xl text-slate-300 md:text-[18px]">
                {option.text[lang]}
              </div>
            </div>
          </button>
        );
      })}
    </div>
  );
}
