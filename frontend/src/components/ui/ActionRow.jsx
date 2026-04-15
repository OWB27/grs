export default function ActionRow({
  children,
  align = "center",
  className = "",
}) {
  const alignClassMap = {
    center: "justify-center",
    between: "justify-between",
    start: "justify-start",
    end: "justify-end",
  };

  const alignClass = alignClassMap[align] || alignClassMap.center;

  return (
    <div className={`flex items-center gap-3 ${alignClass} ${className}`}>
      {children}
    </div>
  );
}