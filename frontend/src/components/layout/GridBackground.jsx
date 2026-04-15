export default function GridBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute inset-0 bg-[#070b11]" />

      <div
        className="absolute inset-0 opacity-[0.045]"
        style={{
          backgroundImage: `
            linear-gradient(rgba(148, 163, 184, 0.28) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148, 163, 184, 0.28) 1px, transparent 1px)
          `,
          backgroundSize: "36px 36px",
          backgroundPosition: "center center",
        }}
      />

      <div className="absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.015),transparent_20%,transparent_80%,rgba(255,255,255,0.01))]" />
    </div>
  );
}