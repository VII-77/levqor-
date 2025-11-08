import type { Metadata } from 'next'
import { Providers } from '@/components/providers'
import Link from 'next/link'
import './globals.css'

export const metadata: Metadata = {
  title: 'Levqor — The self-driven automation engine',
  description: 'Build powerful workflows that run themselves. No code required. Enterprise-grade automation platform trusted by leading teams.',
  openGraph: {
    title: 'Levqor — The self-driven automation engine',
    description: 'Build powerful workflows that run themselves. No code required.',
    url: 'https://levqor.ai',
    siteName: 'Levqor',
    images: [
      {
        url: '/og.png',
        width: 1200,
        height: 630,
        alt: 'Levqor - Automation Engine',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Levqor — The self-driven automation engine',
    description: 'Build powerful workflows that run themselves. No code required.',
    images: ['/og.png'],
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
          <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link href="/" className="text-2xl font-bold text-blue-600">
                Levqor
              </Link>
              <div className="flex items-center gap-6">
                <Link href="/pricing" className="text-gray-700 hover:text-blue-600 font-medium transition">
                  Pricing
                </Link>
                <Link href="/docs" className="text-gray-700 hover:text-blue-600 font-medium transition">
                  Docs
                </Link>
                <Link href="/signin" className="text-gray-700 hover:text-blue-600 font-medium transition">
                  Sign in
                </Link>
                <Link href="/signin" className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
                  Start free
                </Link>
              </div>
            </div>
          </nav>
        </header>

        <Providers>
          {children}
        </Providers>

        <footer className="bg-gray-900 text-gray-300">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="grid md:grid-cols-4 gap-8">
              <div>
                <h3 className="text-white text-lg font-bold mb-4">Levqor</h3>
                <p className="text-sm">The self-driven automation engine for modern teams.</p>
              </div>
              <div>
                <h4 className="text-white font-semibold mb-4">Product</h4>
                <ul className="space-y-2 text-sm">
                  <li><Link href="/pricing" className="hover:text-white transition">Pricing</Link></li>
                  <li><Link href="/docs" className="hover:text-white transition">Documentation</Link></li>
                  <li><a href="https://api.levqor.ai/status" className="hover:text-white transition">Status</a></li>
                </ul>
              </div>
              <div>
                <h4 className="text-white font-semibold mb-4">Legal</h4>
                <ul className="space-y-2 text-sm">
                  <li><Link href="/privacy" className="hover:text-white transition">Privacy</Link></li>
                  <li><Link href="/terms" className="hover:text-white transition">Terms</Link></li>
                </ul>
              </div>
              <div>
                <h4 className="text-white font-semibold mb-4">Support</h4>
                <ul className="space-y-2 text-sm">
                  <li><a href="https://api.levqor.ai/ops/uptime" className="hover:text-white transition">Uptime</a></li>
                  <li><Link href="/contact" className="hover:text-white transition">Contact</Link></li>
                </ul>
              </div>
            </div>
            <div className="border-t border-gray-800 mt-8 pt-8 text-sm text-center">
              <p>&copy; {new Date().getFullYear()} Levqor. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
