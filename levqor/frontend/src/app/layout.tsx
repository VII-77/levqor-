import type { Metadata } from 'next'
import Script from 'next/script'
import './globals.css'

export const metadata: Metadata = {
  title: 'Levqor - AI-Powered Automation Platform',
  description: 'Build powerful automations with natural language. Levqor uses AI to convert your descriptions into production-ready workflows.',
  openGraph: {
    title: 'Levqor - Self-Driving Automation',
    description: 'AI-powered workflow automation that understands plain English',
    url: 'https://levqor.ai',
    siteName: 'Levqor',
    images: [
      {
        url: '/og-launch.png',
        width: 1200,
        height: 630,
      }
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Levqor - Self-Driving Automation',
    description: 'AI-powered workflow automation that understands plain English',
    images: ['/og-launch.png'],
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
          <Script
            defer
            data-domain={plausibleDomain}
            src="https://plausible.io/js/script.js"
          />
        )}
      </head>
      <body>
        <nav style={styles.nav}>
          <div style={styles.navContainer}>
            <a href="/" style={styles.logo}>Levqor</a>
            <div style={styles.navLinks}>
              <a href="/pricing" style={styles.navLink}>Pricing</a>
              <a href="/signup" style={styles.navLink}>Sign Up</a>
              <a href="/dashboard" style={styles.navLink}>Dashboard</a>
            </div>
          </div>
        </nav>
        <main style={styles.main}>{children}</main>
        <footer style={styles.footer}>
          <div style={styles.footerContainer}>
            <div style={styles.footerLinks}>
              <a href="/privacy" style={styles.footerLink}>Privacy</a>
              <a href="/terms" style={styles.footerLink}>Terms</a>
              <a href="/pricing" style={styles.footerLink}>Pricing</a>
              <a href="https://github.com/levqor" style={styles.footerLink}>GitHub</a>
            </div>
            <p style={styles.footerText}>© 2025 Levqor. All rights reserved.</p>
          </div>
        </footer>
      </body>
    </html>
  )
}

const styles = {
  nav: {
    borderBottom: '1px solid #e5e7eb',
    padding: '1rem 0',
  },
  navContainer: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 1rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logo: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    color: '#111827',
    textDecoration: 'none',
  },
  navLinks: {
    display: 'flex',
    gap: '2rem',
  },
  navLink: {
    color: '#4b5563',
    textDecoration: 'none',
    fontSize: '0.95rem',
  },
  main: {
    minHeight: 'calc(100vh - 200px)',
  },
  footer: {
    borderTop: '1px solid #e5e7eb',
    padding: '2rem 0',
    marginTop: '4rem',
  },
  footerContainer: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 1rem',
    textAlign: 'center' as const,
  },
  footerLinks: {
    display: 'flex',
    justifyContent: 'center',
    gap: '2rem',
    marginBottom: '1rem',
  },
  footerLink: {
    color: '#6b7280',
    textDecoration: 'none',
    fontSize: '0.875rem',
  },
  footerText: {
    color: '#9ca3af',
    fontSize: '0.875rem',
  },
}
