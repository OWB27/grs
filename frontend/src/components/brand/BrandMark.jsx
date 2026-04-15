export default function BrandMark() {
  return (
    <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-cyan-400/12 bg-cyan-400/8">
      <svg
        viewBox="0 0 24 24"
        fill="none"
        className="h-5 w-5 text-cyan-300"
        stroke="currentColor"
        strokeWidth="1.7"
      >
        <path d="M12 3.75v4.5" />
        <path d="M12 15.75v4.5" />
        <path d="M3.75 12h4.5" />
        <path d="M15.75 12h4.5" />
        <path d="m7 7 2.2 2.2" />
        <path d="m14.8 14.8 2.2 2.2" />
        <path d="m17 7-2.2 2.2" />
        <path d="m9.2 14.8-2.2 2.2" />
        <circle cx="12" cy="12" r="2.1" />
      </svg>
    </div>
  );
}