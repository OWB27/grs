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
        aria-hidden="true"
        className="h-6 w-6 shrink-0"
      >
        <path
          fill="currentColor"
          fillRule="evenodd"
          clipRule="evenodd"
          d="M12 2C6.76 2 2.45 6.02 2.02 11.15l5.42 2.24a3.29 3.29 0 0 1 1.18-.21l2.42-3.51v-.05a3.84 3.84 0 1 1 3.84 3.84h-.08l-3.45 2.47v.13a2.89 2.89 0 0 1-5.73.53L2.35 15.23A10 10 0 1 0 12 2Zm2.88 5.04a2.58 2.58 0 1 0 0 5.16 2.58 2.58 0 0 0 0-5.16Zm0 .74a1.84 1.84 0 1 1 0 3.68 1.84 1.84 0 0 1 0-3.68ZM7.2 16.38l-1.25-.52c.2.47.58.86 1.08 1.07a2.06 2.06 0 0 0 2.7-1.11 2.05 2.05 0 0 0-1.11-2.69 2 2 0 0 0-1.59-.02l1.29.54a1.49 1.49 0 1 1-1.12 2.73Z"
        />
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
