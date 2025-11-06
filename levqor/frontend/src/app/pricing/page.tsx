'use client'

import { useEffect } from 'react'
import { trackPageView, trackCTAClick } from '@/lib/analytics'

export default function PricingPage() {
  useEffect(() => {
    trackPageView('/pricing')
  }, [])

  const handleCheckout = (plan: string) => {
    trackCTAClick(plan)
    window.location.href = `${process.env.NEXT_PUBLIC_BACKEND_BASE}/api/v1/credits/purchase`
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Simple, Transparent Pricing</h1>
      <p style={styles.subtitle}>Start free, scale as you grow</p>

      <div style={styles.grid}>
        <div style={styles.plan}>
          <h3 style={styles.planName}>Free</h3>
          <div style={styles.price}>
            <span style={styles.priceAmount}>$0</span>
            <span style={styles.pricePeriod}>/forever</span>
          </div>
          <ul style={styles.features}>
            <li>50 free credits</li>
            <li>Basic automations</li>
            <li>Community support</li>
            <li>All integrations</li>
          </ul>
          <a href="/signup" style={styles.freeButton}>
            Get Started
          </a>
        </div>

        <div style={{...styles.plan, ...styles.popularPlan}}>
          <div style={styles.popularBadge}>Popular</div>
          <h3 style={styles.planName}>Credit Pack</h3>
          <div style={styles.price}>
            <span style={styles.priceAmount}>$9</span>
            <span style={styles.pricePeriod}>/100 credits</span>
          </div>
          <ul style={styles.features}>
            <li>100 automation runs</li>
            <li>Never expires</li>
            <li>Priority support</li>
            <li>Advanced features</li>
          </ul>
          <button
            onClick={() => handleCheckout('credit_pack')}
            style={styles.primaryButton}
          >
            Buy Credits
          </button>
        </div>

        <div style={styles.plan}>
          <h3 style={styles.planName}>Enterprise</h3>
          <div style={styles.price}>
            <span style={styles.priceAmount}>Custom</span>
          </div>
          <ul style={styles.features}>
            <li>Unlimited credits</li>
            <li>Dedicated support</li>
            <li>SLA guarantee</li>
            <li>Custom integrations</li>
          </ul>
          <a href="mailto:sales@levqor.ai" style={styles.secondaryButton}>
            Contact Sales
          </a>
        </div>
      </div>

      <div style={styles.faq}>
        <h2 style={styles.faqTitle}>Frequently Asked Questions</h2>
        <div style={styles.faqList}>
          <div style={styles.faqItem}>
            <h3 style={styles.faqQuestion}>What are credits?</h3>
            <p style={styles.faqAnswer}>
              Each automation run costs 1 credit. Credits never expire and can be used across all your workflows.
            </p>
          </div>
          <div style={styles.faqItem}>
            <h3 style={styles.faqQuestion}>Can I get more free credits?</h3>
            <p style={styles.faqAnswer}>
              Yes! Refer friends and earn +20 credits for each signup that becomes active.
            </p>
          </div>
          <div style={styles.faqItem}>
            <h3 style={styles.faqQuestion}>What happens when I run out of credits?</h3>
            <p style={styles.faqAnswer}>
              Your automations will pause. Simply buy more credits to resume. No data is lost.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '4rem 1rem',
  },
  title: {
    fontSize: '3rem',
    fontWeight: 'bold',
    textAlign: 'center' as const,
    marginBottom: '0.5rem',
  },
  subtitle: {
    fontSize: '1.25rem',
    textAlign: 'center' as const,
    color: '#6b7280',
    marginBottom: '4rem',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '2rem',
    marginBottom: '4rem',
  },
  plan: {
    backgroundColor: 'white',
    borderRadius: '0.5rem',
    padding: '2rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    position: 'relative' as const,
  },
  popularPlan: {
    border: '2px solid #2563eb',
  },
  popularBadge: {
    position: 'absolute' as const,
    top: '-12px',
    right: '20px',
    backgroundColor: '#2563eb',
    color: 'white',
    padding: '0.25rem 0.75rem',
    borderRadius: '9999px',
    fontSize: '0.75rem',
    fontWeight: 'bold',
  },
  planName: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    marginBottom: '1rem',
  },
  price: {
    marginBottom: '1.5rem',
  },
  priceAmount: {
    fontSize: '3rem',
    fontWeight: 'bold',
  },
  pricePeriod: {
    fontSize: '1rem',
    color: '#6b7280',
  },
  features: {
    listStyle: 'none',
    marginBottom: '2rem',
    color: '#4b5563',
  },
  freeButton: {
    display: 'block',
    width: '100%',
    padding: '0.75rem',
    backgroundColor: 'transparent',
    color: '#2563eb',
    border: '2px solid #2563eb',
    borderRadius: '0.375rem',
    textAlign: 'center' as const,
    textDecoration: 'none',
    fontSize: '1rem',
    fontWeight: 500,
  },
  primaryButton: {
    width: '100%',
    padding: '0.75rem',
    backgroundColor: '#2563eb',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '1rem',
    fontWeight: 500,
  },
  secondaryButton: {
    display: 'block',
    width: '100%',
    padding: '0.75rem',
    backgroundColor: 'transparent',
    color: '#2563eb',
    border: '2px solid #2563eb',
    borderRadius: '0.375rem',
    textAlign: 'center' as const,
    textDecoration: 'none',
    fontSize: '1rem',
    fontWeight: 500,
  },
  faq: {
    marginTop: '4rem',
  },
  faqTitle: {
    fontSize: '2rem',
    fontWeight: 'bold',
    textAlign: 'center' as const,
    marginBottom: '2rem',
  },
  faqList: {
    maxWidth: '800px',
    margin: '0 auto',
  },
  faqItem: {
    marginBottom: '2rem',
  },
  faqQuestion: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    marginBottom: '0.5rem',
  },
  faqAnswer: {
    color: '#6b7280',
  },
}
