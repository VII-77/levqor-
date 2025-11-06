'use client'

import { useState, useEffect } from 'react'
import { getUser, getSession, signOut } from '@/lib/supabase'
import { useRouter } from 'next/navigation'

interface Subscription {
  plan: string
  status: string
  renews_at: string | null
}

interface UsageData {
  day: string
  jobs_run: number
  cost_saving: number
}

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [subscription, setSubscription] = useState<Subscription | null>(null)
  const [usage, setUsage] = useState<UsageData[]>([])
  const [refCode, setRefCode] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadDashboard()
  }, [])

  async function loadDashboard() {
    try {
      const currentUser = await getUser()
      if (!currentUser) {
        router.push('/signup')
        return
      }

      setUser(currentUser)

      const session = await getSession()
      const token = session?.access_token

      if (!token) {
        router.push('/signup')
        return
      }

      const backendBase = process.env.NEXT_PUBLIC_BACKEND_BASE || ''

      const [subRes, usageRes, refRes] = await Promise.all([
        fetch(`${backendBase}/api/v1/me/subscription`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`${backendBase}/api/v1/me/usage`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`${backendBase}/api/v1/me/referral-code`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ])

      if (subRes.ok) {
        const subData = await subRes.json()
        setSubscription(subData)
      }

      if (usageRes.ok) {
        const usageData = await usageRes.json()
        setUsage(usageData.usage || [])
      }

      if (refRes.ok) {
        const refData = await refRes.json()
        setRefCode(refData.ref_code || '')
      }

    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard')
    } finally {
      setLoading(false)
    }
  }

  async function handleSignOut() {
    await signOut()
    router.push('/')
  }

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loading}>Loading dashboard...</div>
      </div>
    )
  }

  const frontendUrl = process.env.NEXT_PUBLIC_FRONTEND_URL || window.location.origin
  const referralLink = refCode ? `${frontendUrl}/?ref=${refCode}` : ''
  const totalJobs = usage.reduce((sum, day) => sum + day.jobs_run, 0)
  const totalSavings = usage.reduce((sum, day) => sum + day.cost_saving, 0)

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Dashboard</h1>
        <button onClick={handleSignOut} style={styles.signOutButton}>
          Sign Out
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.grid}>
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Account</h2>
          <div style={styles.cardContent}>
            <p><strong>Email:</strong> {user?.email}</p>
            <p><strong>Plan:</strong> {subscription?.plan || 'Free'}</p>
            <p><strong>Status:</strong> {subscription?.status || 'Active'}</p>
            {subscription?.renews_at && (
              <p><strong>Renews:</strong> {new Date(subscription.renews_at).toLocaleDateString()}</p>
            )}
          </div>
        </div>

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Usage (Last 14 Days)</h2>
          <div style={styles.cardContent}>
            <div style={styles.stat}>
              <span style={styles.statValue}>{totalJobs}</span>
              <span style={styles.statLabel}>Total Jobs</span>
            </div>
            <div style={styles.stat}>
              <span style={styles.statValue}>${totalSavings.toFixed(2)}</span>
              <span style={styles.statLabel}>Cost Savings</span>
            </div>
          </div>
        </div>

        {referralLink && (
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Referral Link</h2>
            <div style={styles.cardContent}>
              <p style={styles.referralText}>Share this link to earn credits:</p>
              <div style={styles.referralLink}>
                <input
                  type="text"
                  value={referralLink}
                  readOnly
                  style={styles.referralInput}
                  onClick={(e) => (e.target as HTMLInputElement).select()}
                />
                <button
                  onClick={() => navigator.clipboard.writeText(referralLink)}
                  style={styles.copyButton}
                >
                  Copy
                </button>
              </div>
              <p style={styles.referralReward}>Get +20 credits for each signup!</p>
            </div>
          </div>
        )}

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Daily Activity</h2>
          <div style={styles.cardContent}>
            {usage.length === 0 ? (
              <p style={styles.emptyState}>No activity yet. Start building automations!</p>
            ) : (
              <div style={styles.usageList}>
                {usage.map((day) => (
                  <div key={day.day} style={styles.usageItem}>
                    <span>{day.day}</span>
                    <span>{day.jobs_run} jobs</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <div style={styles.actions}>
        <a href="/pricing" style={styles.upgradeButton}>
          Upgrade Plan
        </a>
        <a href="https://api.levqor.ai/docs" style={styles.docsButton}>
          API Docs
        </a>
      </div>
    </div>
  )
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '2rem 1rem',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '2rem',
  },
  title: {
    fontSize: '2rem',
    fontWeight: 'bold',
  },
  signOutButton: {
    padding: '0.5rem 1rem',
    backgroundColor: '#ef4444',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
  },
  loading: {
    textAlign: 'center' as const,
    padding: '4rem 0',
    fontSize: '1.125rem',
    color: '#6b7280',
  },
  error: {
    backgroundColor: '#fee2e2',
    color: '#991b1b',
    padding: '1rem',
    borderRadius: '0.375rem',
    marginBottom: '1rem',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '1.5rem',
    marginBottom: '2rem',
  },
  card: {
    backgroundColor: 'white',
    borderRadius: '0.5rem',
    padding: '1.5rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  cardTitle: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    marginBottom: '1rem',
  },
  cardContent: {
    color: '#4b5563',
  },
  stat: {
    display: 'flex',
    flexDirection: 'column' as const,
    marginBottom: '1rem',
  },
  statValue: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#2563eb',
  },
  statLabel: {
    fontSize: '0.875rem',
    color: '#6b7280',
  },
  referralText: {
    marginBottom: '0.5rem',
    fontSize: '0.875rem',
  },
  referralLink: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '0.5rem',
  },
  referralInput: {
    flex: 1,
    padding: '0.5rem',
    border: '1px solid #d1d5db',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
  },
  copyButton: {
    padding: '0.5rem 1rem',
    backgroundColor: '#2563eb',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
  },
  referralReward: {
    fontSize: '0.75rem',
    color: '#059669',
    fontWeight: 500,
  },
  usageList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.5rem',
  },
  usageItem: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '0.5rem',
    backgroundColor: '#f9fafb',
    borderRadius: '0.25rem',
    fontSize: '0.875rem',
  },
  emptyState: {
    textAlign: 'center' as const,
    color: '#9ca3af',
    padding: '2rem 0',
  },
  actions: {
    display: 'flex',
    gap: '1rem',
    justifyContent: 'center',
  },
  upgradeButton: {
    padding: '0.75rem 2rem',
    backgroundColor: '#2563eb',
    color: 'white',
    borderRadius: '0.375rem',
    textDecoration: 'none',
    fontSize: '1rem',
    fontWeight: 500,
  },
  docsButton: {
    padding: '0.75rem 2rem',
    backgroundColor: 'transparent',
    color: '#2563eb',
    border: '2px solid #2563eb',
    borderRadius: '0.375rem',
    textDecoration: 'none',
    fontSize: '1rem',
    fontWeight: 500,
  },
}
