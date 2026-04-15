import { useState } from "react";

export default function useQuizFlow({
  questions,
  validationMessage,
  onSubmit,
  submitDelayMs = 700,
}) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const totalQuestions = questions.length;
  const currentQuestion = questions[currentQuestionIndex];
  const currentQuestionId = currentQuestion.id;
  const selectedOptionId = answers[currentQuestionId];
  const currentStep = currentQuestionIndex + 1;
  const isFirstQuestion = currentQuestionIndex === 0;
  const isLastQuestion = currentQuestionIndex === totalQuestions - 1;

  function validateCurrentSelection() {
    if (selectedOptionId) {
      return true;
    }

    setSubmitError(validationMessage);
    return false;
  }

  function handleSelect(optionId) {
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
      return;
    }

    setCurrentQuestionIndex((prev) => prev + 1);
    setSubmitError("");
  }

  function handleSubmit() {
    if (!validateCurrentSelection()) {
      return;
    }

    setSubmitError("");
    setIsSubmitting(true);

    const finalAnswers = {
      ...answers,
      [currentQuestionId]: selectedOptionId,
    };

    setTimeout(() => {
      onSubmit(finalAnswers);
    }, submitDelayMs);
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
