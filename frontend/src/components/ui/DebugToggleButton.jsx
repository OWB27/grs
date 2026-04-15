export default function DebugToggleButton({ isOpen, onClick, ariaLabel }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="inline-flex h-[52px] w-[52px] items-center justify-center rounded-xl border border-white/8 bg-black/20 text-white transition hover:border-white/14 hover:bg-white/[0.04]"
      aria-label={ariaLabel}
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        className="h-5 w-5"
        stroke="currentColor"
        strokeWidth="2"
      >
        {isOpen ? (
          <path d="m6 15 6-6 6 6" />
        ) : (
          <path d="m6 9 6 6 6-6" />
        )}
      </svg>
    </button>
  );
}