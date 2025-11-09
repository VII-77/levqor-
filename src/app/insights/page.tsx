export default function Insights() {
  return (
    <main className="p-8 max-w-3xl mx-auto">
      <h1 className="text-2xl font-semibold">Operational Insights</h1>
      <p className="mt-2 text-slate-600">Live health, latency, and recent incidents.</p>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <a className="border rounded p-4 hover:bg-slate-50" href="https://api.levqor.ai/ops/uptime">Uptime</a>
        <a className="border rounded p-4 hover:bg-slate-50" href="https://api.levqor.ai/status">Status JSON</a>
      </div>
    </main>
  );
}
