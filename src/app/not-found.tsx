export default function NotFound() {
  return (
    <main className="min-h-screen flex items-center justify-center p-10">
      <div className="max-w-xl text-center space-y-4">
        <div className="text-xs uppercase tracking-widest opacity-60">Levqor</div>
        <h1 className="text-3xl font-semibold">Page not found</h1>
        <p className="opacity-80">The page you requested isn’t here. Try the dashboard, pricing, or docs.</p>
        <div className="flex gap-3 justify-center">
          <a className="px-4 py-2 rounded bg-black text-white" href="/signin">Sign in</a>
          <a className="px-4 py-2 rounded border" href="/pricing">Pricing</a>
          <a className="px-4 py-2 rounded border" href="/docs">Docs</a>
        </div>
      </div>
    </main>
  );
}
