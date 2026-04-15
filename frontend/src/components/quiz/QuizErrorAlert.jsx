export default function QuizErrorAlert({ message }) {
  if (!message) {
    return null;
  }

  return (
    <div className="mt-5 rounded-xl border border-red-400/12 bg-red-400/[0.05] px-4 py-3 text-sm text-red-200">
      {message}
    </div>
  );
}
