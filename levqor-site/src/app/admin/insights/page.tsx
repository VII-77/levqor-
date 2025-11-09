export default function AdminInsights() {
  return (
    <main className="p-8 max-w-3xl mx-auto">
      <h1 className="text-2xl font-semibold">Admin Intelligence</h1>
      <p className="mt-2 text-slate-600">Feature flags, runbooks, weekly briefs.</p>
      <ul className="mt-6 list-disc pl-6 space-y-2">
        <li><code>https://api.levqor.ai/api/admin/flags</code></li>
        <li><code>https://api.levqor.ai/api/admin/runbooks</code></li>
      </ul>
    </main>
  );
}
