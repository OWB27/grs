import PanelCard from "../ui/PanelCard";

export default function EmptyStatePanel({
  code,
  message,
  actions,
  className = "",
}) {
  return (
    <PanelCard className={`mx-auto max-w-2xl p-8 text-center ${className}`}>
      {code ? (
        <div className="font-mono text-xs tracking-wide text-slate-500">
          {code}
        </div>
      ) : null}

      <p className="mt-4 text-slate-300">{message}</p>

      {actions ? <div className="mt-6">{actions}</div> : null}
    </PanelCard>
  );
}