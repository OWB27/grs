export default function PanelCard({ children, className = "" }) {
  return (
    <section
      className={`rounded-[24px] border border-white/8 bg-white/[0.025] p-5 shadow-[0_8px_40px_rgba(0,0,0,0.28)] backdrop-blur-sm ${className}`}
    >
      {children}
    </section>
  );
}