import { Routes, Route } from "react-router";
import HomePage from "./pages/HomePage";
import MethodologyPage from "./pages/MethodologyPage";
import QuizPage from "./pages/QuizPage";
import ResultPage from "./pages/ResultPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/methodology" element={<MethodologyPage />} />
      <Route path="/quiz" element={<QuizPage />} />
      <Route path="/result" element={<ResultPage />} />
    </Routes>
  );
}
