export default function PageSection({
  children,
  width = "lg",
  centered = false,
  className = "",
}) {
  const widthClassMap = {
    sm: "max-w-2xl",
    md: "max-w-3xl",
    lg: "max-w-5xl",
    xl: "max-w-6xl",
  };

  const widthClass = widthClassMap[width] || widthClassMap.lg;

  return (
    <section
      className={`mx-auto w-full ${widthClass} ${
        centered ? "text-center" : ""
      } ${className}`}
    >
      {children}
    </section>
  );
}