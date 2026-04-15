import { Link } from "react-router";

export default function PrimaryButton({
  children,
  to,
  onClick,
  type = "button",
  disabled = false,
  className = "",
}) {
  const baseClassName =
    "inline-flex items-center justify-center gap-2 rounded-lg border border-cyan-300/15 bg-cyan-400 px-5 py-2.5 text-sm font-semibold text-slate-950 shadow-[0_6px_20px_rgba(34,211,238,0.22)] transition duration-200 hover:bg-cyan-300 hover:shadow-[0_8px_24px_rgba(34,211,238,0.28)] disabled:cursor-not-allowed disabled:opacity-50";

  if (to) {
    return (
      <Link to={to} className={`${baseClassName} ${className}`}>
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
      {children}
    </button>
  );
}