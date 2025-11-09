async function getStatus() {
  try {
    const r = await fetch("https://api.levqor.ai/status", { next: { revalidate: 30 }});
    return r.ok ? "Operational" : "Degraded";
  } catch { return "Unknown"; }
}
export default async function Home() {
  const status = await getStatus();
  return (
    <main className="min-h-screen">
      <section className="px-6 py-20 text-center bg-gradient-to-b from-slate-50 to-white">
        <div className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-sm">
          <span className={`size-2 rounded-full ${status==="Operational"?"bg-green-500":"bg-yellow-500"}`}></span>
          <span>Systems: {status}</span>
        </div>
        <h1 className="mt-6 text-5xl font-semibold">Self-Driven Automation for Teams</h1>
        <p className="mt-4 text-slate-600">Integrate. Orchestrate. Observe. Levqor runs your workflows and heals itself.</p>
        <div className="mt-6 flex gap-3 justify-center">
          <a className="px-5 py-3 rounded bg-black text-white" href="/signin">Start free</a>
          <a className="px-5 py-3 rounded border" href="/pricing">See pricing</a>
        </div>
        <p className="mt-3 text-xs text-slate-500">GDPR • SSO • Stripe • Sentry</p>
      </section>
    </main>
  );
}
