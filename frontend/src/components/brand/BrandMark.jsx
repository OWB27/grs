export default function BrandMark() {
  return (
    <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-cyan-400/15 bg-[radial-gradient(circle_at_50%_50%,rgba(15,45,58,0.96),rgba(7,11,17,0.98)_72%)] shadow-[inset_0_1px_0_rgba(255,255,255,0.08),0_0_24px_rgba(34,211,238,0.12)]">
      <svg
        viewBox="0 0 36 36"
        fill="none"
        className="h-7 w-7"
        aria-hidden="true"
      >
        <defs>
          <linearGradient
            id="grs-radar-sweep"
            x1="18"
            y1="18"
            x2="30"
            y2="10"
            gradientUnits="userSpaceOnUse"
          >
            <stop stopColor="#22d3ee" stopOpacity="0.38" />
            <stop offset="1" stopColor="#47d85a" stopOpacity="0.1" />
          </linearGradient>
        </defs>

        <circle
          cx="18"
          cy="18"
          r="12.75"
          fill="#07111d"
          stroke="#67e8f9"
          strokeOpacity="0.62"
          strokeWidth="1.5"
        />
        <circle
          cx="18"
          cy="18"
          r="8.15"
          stroke="#67e8f9"
          strokeOpacity="0.18"
          strokeWidth="1"
        />
        <circle
          cx="18"
          cy="18"
          r="4.15"
          stroke="#67e8f9"
          strokeOpacity="0.22"
          strokeWidth="1"
        />
        <path
          d="M18 18 27.9 10.4A12.75 12.75 0 0 1 30.72 20.35L18 18Z"
          fill="url(#grs-radar-sweep)"
        />
        <path
          d="M18 5.25v25.5M5.25 18h25.5"
          stroke="#67e8f9"
          strokeOpacity="0.2"
          strokeWidth="1"
        />
        <path
          d="M18 18 28.35 10.05"
          stroke="#22d3ee"
          strokeLinecap="round"
          strokeWidth="2"
        />
        <path
          d="M29.2 18h-4.55"
          stroke="#47d85a"
          strokeLinecap="round"
          strokeWidth="2"
        />
        <circle
          cx="18"
          cy="18"
          r="2"
          fill="#e0faff"
        />
        <circle
          cx="26.45"
          cy="11.55"
          r="2.65"
          fill="#47d85a"
          stroke="#d9ffe1"
          strokeOpacity="0.85"
          strokeWidth="0.8"
        />
        <circle
          cx="11.1"
          cy="22.35"
          r="1.5"
          fill="#22d3ee"
          fillOpacity="0.9"
        />
      </svg>
    </div>
  );
}
