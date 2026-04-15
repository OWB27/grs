import { useTranslation } from "react-i18next";

export default function LanguageSwitcher() {
  const { i18n, t } = useTranslation();
  const currentLang = i18n.language;

  return (
    <div className="flex items-center gap-2 text-sm text-slate-400">
      <button
        type="button"
        onClick={() => i18n.changeLanguage("en")}
        aria-label={t("language.switchToEnglish")}
        className={`transition ${
          currentLang === "en" ? "text-white" : "text-slate-500 hover:text-slate-300"
        }`}
      >
        {t("language.englishShort")}
      </button>

      <span className="text-slate-600">/</span>

      <button
        type="button"
        onClick={() => i18n.changeLanguage("zh")}
        aria-label={t("language.switchToChinese")}
        className={`transition ${
          currentLang === "zh" ? "text-white" : "text-slate-500 hover:text-slate-300"
        }`}
      >
        {t("language.chineseShort")}
      </button>
    </div>
  );
}
