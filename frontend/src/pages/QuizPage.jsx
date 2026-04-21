import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";

import AppShell from "../components/layout/AppShell";
import PageSection from "../components/layout/PageSection";
import TopNav from "../components/common/TopNav";
import EmptyStatePanel from "../components/common/EmptyStatePanel";
import ProgressBar from "../components/quiz/ProgressBar";
import QuestionCard from "../components/quiz/QuestionCard";
import QuizActions from "../components/quiz/QuizActions";
import QuizErrorAlert from "../components/quiz/QuizErrorAlert";
import useQuizFlow from "../hooks/useQuizFlow";
import { fetchQuestions, fetchRecommendations } from "../lib/api";

export default function QuizPage() {
  const { i18n, t } = useTranslation();
  const navigate = useNavigate();
  const lang = i18n.language;

  const [questions, setQuestions] = useState([]);
  const [isLoadingQuestions, setIsLoadingQuestions] = useState(true);
  const [questionsError, setQuestionsError] = useState("");

  useEffect(() => {
    let ignore = false;

    async function loadQuestions() {
      try {
        setIsLoadingQuestions(true);
        setQuestionsError("");

        const data = await fetchQuestions();

        if (!ignore) {
          setQuestions(data.questions ?? []);
        }
      } catch (error) {
        if (!ignore) {
          setQuestionsError(error?.message || t("questionsLoadError"));
        }
      } finally {
        if (!ignore) {
          setIsLoadingQuestions(false);
        }
      }
    }

    loadQuestions();

    return () => {
      ignore = true;
    };
  }, [t]);

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
    onSubmit: async (finalAnswers) => {
      const payload = {
        answers: Object.entries(finalAnswers).map(([questionId, optionId]) => ({
          questionId: Number(questionId),
          optionId: Number(optionId),
        })),
      };

      const data = await fetchRecommendations(payload);

      navigate("/result", {
        state: {
          recommendations: data.recommendations,
          answers: finalAnswers,
        },
      });
    },
  });

  return (
    <AppShell>
      <TopNav />

      <PageSection width="lg" className="flex flex-col items-center">
        {isLoadingQuestions ? (
          <EmptyStatePanel
            code="LOADING_QUESTIONS"
            message={t("loadingQuestions")}
          />
        ) : questionsError ? (
          <EmptyStatePanel
            code="QUESTIONS_ERROR"
            message={questionsError}
          />
        ) : currentQuestion ? (
          <>
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
          </>
        ) : (
          <EmptyStatePanel
            code="NO_QUESTIONS"
            message={t("questionsLoadError")}
          />
        )}
      </PageSection>
    </AppShell>
  );
}