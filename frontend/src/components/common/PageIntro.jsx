export default function PageIntro({
  code,
  title,
  subtitle,
  centered = false,
  className = "",
}) {
  return (
    <div className={`${centered ? "text-center" : ""} ${className}`}>
      {code ? (
        <div className="font-mono text-xs tracking-wide text-slate-500">
          {code}
        </div>
      ) : null}

      <h1 className="mt-3 text-4xl font-semibold tracking-tight text-white md:text-5xl">
        {title}
      </h1>

      {subtitle ? (
        <p
          className={`mt-4 text-sm leading-7 text-slate-400 md:text-base ${
            centered ? "mx-auto max-w-2xl" : "max-w-2xl"
          }`}
        >
          {subtitle}
        </p>
      ) : null}
    </div>
  );
}