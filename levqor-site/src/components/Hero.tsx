import Link from 'next/link';
import StatusPill from './StatusPill';

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white">
      <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10" />
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
        <div className="text-center space-y-8">
          <StatusPill />
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight">
            The Self-Driven
            <br />
            <span className="text-blue-200">Automation Engine</span>
          </h1>
          <p className="max-w-2xl mx-auto text-xl sm:text-2xl text-blue-100">
            Build powerful workflows that run themselves. No code required. Just results.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              href="/signin"
              className="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg hover:bg-blue-50 transition shadow-xl hover:shadow-2xl"
            >
              Start Free Trial
            </Link>
            <Link
              href="/pricing"
              className="px-8 py-4 bg-blue-500/20 backdrop-blur-sm text-white rounded-lg font-semibold text-lg hover:bg-blue-500/30 transition border border-white/20"
            >
              View Pricing
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
