import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";

import AppShell from "../components/layout/AppShell";
import PageSection from "../components/layout/PageSection";
import TopNav from "../components/common/TopNav";
import ProgressBar from "../components/quiz/ProgressBar";
import QuestionCard from "../components/quiz/QuestionCard";
import QuizActions from "../components/quiz/QuizActions";
import QuizErrorAlert from "../components/quiz/QuizErrorAlert";
import { mockQuestions } from "../data/mockQuestions";
import { getMockRecommendations } from "../data/mockResults";
import useQuizFlow from "../hooks/useQuizFlow";

export default function QuizPage() {
  const { i18n, t } = useTranslation();
  const navigate = useNavigate();

  const questions = mockQuestions;
  const lang = i18n.language;
  const {
    currentQuestion,
    currentStep,
    totalQuestions,
    selectedOptionId,
    submitError,
    isSubmitting,
    isFirstQuestion,
    isLastQuestion,
    handleSelect,
    handlePrevious,
    handleNext,
    handleSubmit,
  } = useQuizFlow({
    questions,
    validationMessage: t("quiz.error.selectOption"),
    onSubmit: (finalAnswers) => {
      const recommendations = getMockRecommendations(finalAnswers);

      navigate("/result", {
        state: {
          recommendations,
          answers: finalAnswers,
        },
      });
    },
  });

  return (
    <AppShell>
      <TopNav />

      <PageSection width="lg" className="flex flex-col items-center">
        <div className="mb-10 md:mb-12">
          <ProgressBar current={currentStep} total={totalQuestions} />
        </div>

        <div className="w-full">
          <QuestionCard
            question={currentQuestion}
            selectedOptionId={selectedOptionId}
            onSelect={handleSelect}
            lang={lang}
          />
        </div>

        <QuizErrorAlert message={submitError} />

        <QuizActions
          isFirstQuestion={isFirstQuestion}
          isLastQuestion={isLastQuestion}
          isSubmitting={isSubmitting}
          onPrevious={handlePrevious}
          onNext={handleNext}
          onSubmit={handleSubmit}
        />
      </PageSection>
    </AppShell>
  );
}
