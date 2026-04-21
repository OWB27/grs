const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

let questionsCache = null;
let questionsPromise = null;

async function getErrorMessage(response) {
  try {
    const data = await response.json();
    return data.message || data.detail || `Request failed with status ${response.status}.`;
  } catch {
    return `Request failed with status ${response.status}.`;
  }
}

async function requestJson(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);

  if (!response.ok) {
    throw new ApiError(await getErrorMessage(response), response.status);
  }

  return response.json();
}

export function clearQuestionsCache() {
  questionsCache = null;
  questionsPromise = null;
}

export async function fetchQuestions({ forceRefresh = false } = {}) {
  if (!forceRefresh && questionsCache) {
    return questionsCache;
  }

  if (!forceRefresh && questionsPromise) {
    return questionsPromise;
  }

  questionsPromise = requestJson("/questions")
    .then((data) => {
      questionsCache = data;
      return data;
    })
    .finally(() => {
      questionsPromise = null;
    });

  return questionsPromise;
}

export async function prefetchQuestions() {
  try {
    await fetchQuestions();
  } catch (error) {
    console.warn("Questions prefetch failed:", error);
  }
}

export async function fetchRecommendations(payload) {
  return requestJson("/recommend", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}