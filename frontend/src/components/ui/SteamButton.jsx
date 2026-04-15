import { useTranslation } from "react-i18next";

export default function SteamButton({ href }) {
  const { t } = useTranslation();

  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      className="inline-flex h-[52px] flex-1 items-center justify-center gap-3 rounded-xl bg-[#14253b] px-5 text-lg font-semibold text-slate-100 transition hover:bg-[#19304d]"
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        className="h-5 w-5"
        stroke="currentColor"
        strokeWidth="1.8"
      >
        <circle cx="10" cy="14" r="3.5" />
        <path d="M13 12.5 18 10" />
        <circle cx="18.5" cy="9.5" r="2.75" />
        <path d="M7 16l-2.5-1.5" />
      </svg>

      <span>{t("result.steamStore")}</span>

      <svg
        viewBox="0 0 24 24"
        fill="none"
        className="h-5 w-5"
        stroke="currentColor"
        strokeWidth="2"
      >
        <path d="M7 17 17 7" />
        <path d="M8 7h9v9" />
      </svg>
    </a>
  );
}