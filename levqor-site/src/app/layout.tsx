import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Levqor — The Self-Driven Automation Engine',
  description: 'Automate your business with AI-powered workflows. No cron jobs, no plugins. Just intelligent automation that runs itself.',
  keywords: ['automation', 'AI', 'workflow', 'zapier alternative', 'make.com alternative', 'business automation'],
  openGraph: {
    title: 'Levqor — The Self-Driven Automation Engine',
    description: 'Automate your business with AI-powered workflows. No cron jobs, no plugins.',
    url: 'https://levqor.ai',
    siteName: 'Levqor',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Levqor — The Self-Driven Automation Engine',
    description: 'Automate your business with AI-powered workflows. No cron jobs, no plugins.',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const plausibleDomain = process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN

  return (
    <html lang="en">
      <head>
        {plausibleDomain && (
          <script defer data-domain={plausibleDomain} src="https://plausible.io/js/script.js"></script>
        )}
      </head>
      <body style={{
        margin: 0,
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        backgroundColor: '#000',
        color: '#fff',
        minHeight: '100vh'
      }}>
        {children}
      </body>
    </html>
  )
}
