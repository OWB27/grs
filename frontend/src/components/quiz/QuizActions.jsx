import { useTranslation } from "react-i18next";

import ActionRow from "../ui/ActionRow";
import PrimaryButton from "../ui/PrimaryButton";
import SecondaryButton from "../ui/SecondaryButton";

function PreviousIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      className="h-4.5 w-4.5"
      stroke="currentColor"
      strokeWidth="2"
    >
      <path d="M19 12H6" />
      <path d="m11 6-6 6 6 6" />
    </svg>
  );
}

function NextIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      className="h-4.5 w-4.5"
      stroke="currentColor"
      strokeWidth="2"
    >
      <path d="M5 12h13" />
      <path d="m13 6 6 6-6 6" />
    </svg>
  );
}

export default function QuizActions({
  isFirstQuestion,
  isLastQuestion,
  isSubmitting,
  onPrevious,
  onNext,
  onSubmit,
}) {
  const { t } = useTranslation();

  return (
    <ActionRow className="mt-10">
      <SecondaryButton
        onClick={onPrevious}
        disabled={isFirstQuestion || isSubmitting}
        icon={<PreviousIcon />}
      >
        {t("previous")}
      </SecondaryButton>

      {!isLastQuestion ? (
        <PrimaryButton onClick={onNext} disabled={isSubmitting}>
          {t("next")}
          <NextIcon />
        </PrimaryButton>
      ) : (
        <PrimaryButton onClick={onSubmit} disabled={isSubmitting}>
          {isSubmitting ? t("submitting") : t("submit")}
        </PrimaryButton>
      )}
    </ActionRow>
  );
}
