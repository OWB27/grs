import GridBackground from "./GridBackground";

export default function AppShell({ children }) {
  return (
    <main className="relative min-h-screen overflow-hidden bg-[#070b11] text-slate-100">
      <GridBackground />

      <div className="relative z-10 mx-auto max-w-6xl px-5 py-6 md:px-7 lg:px-8">
        {children}
      </div>
    </main>
  );
}