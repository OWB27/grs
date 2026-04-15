import { Link } from "react-router";

export default function SecondaryButton({
  children,
  to,
  onClick,
  type = "button",
  disabled = false,
  className = "",
  icon,
}) {
  const baseClassName =
    "inline-flex items-center justify-center gap-2 rounded-xl border border-white/8 bg-white/[0.02] px-6 py-3 text-sm font-semibold text-slate-300 transition hover:border-white/14 hover:bg-white/[0.04] disabled:cursor-not-allowed disabled:opacity-40";

  if (to) {
    return (
      <Link to={to} className={`${baseClassName} ${className}`}>
        {icon ? icon : null}
        {children}
      </Link>
    );
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClassName} ${className}`}
    >
      {icon ? icon : null}
      {children}
    </button>
  );
}