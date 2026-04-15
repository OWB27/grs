import { useEffect, useMemo, useState } from "react";

export default function useQuizFlow({
  questions = [],
  validationMessage,
  onSubmit,
}) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 当题目数据变化时，重置流程
  useEffect(() => {
    setCurrentQuestionIndex(0);
    setAnswers({});
    setSubmitError("");
    setIsSubmitting(false);
  }, [questions]);

  const totalQuestions = questions.length;

  const currentQuestion = useMemo(() => {
    if (totalQuestions === 0) return null;
    return questions[currentQuestionIndex] ?? null;
  }, [questions, currentQuestionIndex, totalQuestions]);

  const currentQuestionId = currentQuestion?.id;
  const selectedOptionId = currentQuestionId ? answers[currentQuestionId] : undefined;
  const currentStep = totalQuestions === 0 ? 0 : currentQuestionIndex + 1;
  const isFirstQuestion = currentQuestionIndex === 0;
  const isLastQuestion =
    totalQuestions > 0 && currentQuestionIndex === totalQuestions - 1;

  function validateCurrentSelection() {
    if (!currentQuestion) {
      setSubmitError(validationMessage);
      return false;
    }

    if (selectedOptionId) {
      return true;
    }

    setSubmitError(validationMessage);
    return false;
  }

  function handleSelect(optionId) {
    if (!currentQuestionId) return;

    setAnswers((prev) => ({
      ...prev,
      [currentQuestionId]: optionId,
    }));
    setSubmitError("");
  }

  function handlePrevious() {
    if (isFirstQuestion || isSubmitting) {
      return;
    }

    setCurrentQuestionIndex((prev) => prev - 1);
    setSubmitError("");
  }

  function handleNext() {
    if (!validateCurrentSelection()) {
      return false;
    }

    setCurrentQuestionIndex((prev) => prev + 1);
    setSubmitError("");
    return true;
  }

  async function handleSubmit() {
    if (!validateCurrentSelection()) {
      return;
    }

    if (!currentQuestionId) {
      return;
    }

    setSubmitError("");
    setIsSubmitting(true);

    const finalAnswers = {
      ...answers,
      [currentQuestionId]: selectedOptionId,
    };

    try {
      await onSubmit(finalAnswers);
    } catch (error) {
      setSubmitError(error?.message || validationMessage);
    } finally {
      setIsSubmitting(false);
    }
  }

  return {
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
  };
}