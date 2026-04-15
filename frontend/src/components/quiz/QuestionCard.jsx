import OptionList from "./OptionList";

export default function QuestionCard({
  question,
  selectedOptionId,
  onSelect,
  lang,
}) {
  return (
    <section className="rounded-[28px] border border-cyan-400/10 bg-[linear-gradient(90deg,rgba(17,54,66,0.78),rgba(15,24,39,0.90),rgba(17,54,66,0.78))] px-6 py-10 shadow-[0_10px_60px_rgba(0,0,0,0.28)] md:px-12 md:py-14">
      <h2 className="mx-auto mb-10 max-w-3xl text-center text-3xl font-semibold tracking-tight text-white md:mb-12 md:text-4xl">
        {question.title[lang]}
      </h2>

      <div className="mx-auto max-w-4xl">
        <OptionList
          options={question.options}
          selectedOptionId={selectedOptionId}
          onSelect={onSelect}
          lang={lang}
        />
      </div>
    </section>
  );
}