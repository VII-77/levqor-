'use client'

import { useEffect } from 'react'
import { captureReferralParams } from '@/lib/referrals'
import { trackPageView } from '@/lib/analytics'

export default function HomePage() {
  useEffect(() => {
    captureReferralParams()
    trackPageView('/')
  }, [])

  return (
    <div style={styles.container}>
      <section style={styles.hero}>
        <h1 style={styles.title}>
          AI-Powered Automation<br/>That Understands You
        </h1>
        <p style={styles.subtitle}>
          Describe your workflow in plain English. Levqor's AI converts it into production-ready automation in seconds.
        </p>
        <div style={styles.ctas}>
          <a href="/signup" style={styles.primaryButton}>
            Get Started Free
          </a>
          <a href="/pricing" style={styles.secondaryButton}>
            View Pricing
          </a>
        </div>
      </section>

      <section style={styles.features}>
        <div style={styles.feature}>
          <h3 style={styles.featureTitle}>🤖 Natural Language</h3>
          <p style={styles.featureText}>
            Just describe what you want: "Every morning, send me HN top posts in Slack"
          </p>
        </div>
        <div style={styles.feature}>
          <h3 style={styles.featureTitle}>⚡ Instant Setup</h3>
          <p style={styles.featureText}>
            No complex configuration. AI generates complete workflows in 30 seconds.
          </p>
        </div>
        <div style={styles.feature}>
          <h3 style={styles.featureTitle}>🔗 50+ Integrations</h3>
          <p style={styles.featureText}>
            Connect Slack, Notion, Gmail, and more. All your tools in one place.
          </p>
        </div>
      </section>

      <section style={styles.cta}>
        <h2 style={styles.ctaTitle}>Start Building Today</h2>
        <p style={styles.ctaText}>50 free credits. No credit card required.</p>
        <a href="/signup" style={styles.primaryButton}>
          Sign Up Now
        </a>
      </section>
    </div>
  )
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 1rem',
  },
  hero: {
    textAlign: 'center' as const,
    padding: '4rem 0',
  },
  title: {
    fontSize: '3rem',
    fontWeight: 'bold',
    marginBottom: '1.5rem',
    lineHeight: 1.2,
  },
  subtitle: {
    fontSize: '1.25rem',
    color: '#6b7280',
    marginBottom: '2rem',
    maxWidth: '700px',
    margin: '0 auto 2rem',
  },
  ctas: {
    display: 'flex',
    gap: '1rem',
    justifyContent: 'center',
  },
  primaryButton: {
    padding: '0.75rem 2rem',
    backgroundColor: '#2563eb',
    color: 'white',
    borderRadius: '0.5rem',
    fontSize: '1rem',
    fontWeight: 500,
    textDecoration: 'none',
    display: 'inline-block',
  },
  secondaryButton: {
    padding: '0.75rem 2rem',
    backgroundColor: 'transparent',
    color: '#2563eb',
    border: '2px solid #2563eb',
    borderRadius: '0.5rem',
    fontSize: '1rem',
    fontWeight: 500,
    textDecoration: 'none',
    display: 'inline-block',
  },
  features: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '2rem',
    padding: '4rem 0',
  },
  feature: {
    textAlign: 'center' as const,
  },
  featureTitle: {
    fontSize: '1.5rem',
    marginBottom: '0.5rem',
  },
  featureText: {
    color: '#6b7280',
  },
  cta: {
    textAlign: 'center' as const,
    padding: '4rem 0',
    backgroundColor: '#f9fafb',
    borderRadius: '1rem',
    margin: '2rem 0',
  },
  ctaTitle: {
    fontSize: '2rem',
    marginBottom: '1rem',
  },
  ctaText: {
    fontSize: '1.125rem',
    color: '#6b7280',
    marginBottom: '2rem',
  },
}
