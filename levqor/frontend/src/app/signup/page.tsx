'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { submitReferral } from '@/lib/referrals'
import { trackSignupEvent } from '@/lib/analytics'
import { useRouter } from 'next/navigation'

export default function SignupPage() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()

  useEffect(() => {
    trackSignupEvent('start')
  }, [])

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    setError('')

    try {
      const { data, error } = await supabase.auth.signInWithOtp({
        email,
        options: {
          emailRedirectTo: `${window.location.origin}/dashboard`
        }
      })

      if (error) throw error

      setMessage('Check your email for the magic link!')
      trackSignupEvent('success', email)
      
      await submitReferral(email)
      
    } catch (err: any) {
      setError(err.message || 'Failed to send magic link')
    } finally {
      setLoading(false)
    }
  }

  const handleGoogleSignup = async () => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/dashboard`
        }
      })
      if (error) throw error
    } catch (err: any) {
      setError(err.message || 'Failed to sign up with Google')
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Sign Up for Levqor</h1>
        <p style={styles.subtitle}>Get started with 50 free credits</p>

        {message && (
          <div style={styles.success}>{message}</div>
        )}

        {error && (
          <div style={styles.error}>{error}</div>
        )}

        <form onSubmit={handleSignup} style={styles.form}>
          <input
            type="email"
            placeholder="your@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={styles.input}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            style={styles.button}
          >
            {loading ? 'Sending...' : 'Send Magic Link'}
          </button>
        </form>

        <div style={styles.divider}>or</div>

        <button
          onClick={handleGoogleSignup}
          style={styles.googleButton}
        >
          <span style={styles.googleIcon}>G</span> Sign up with Google
        </button>

        <p style={styles.footer}>
          Already have an account? <a href="/login" style={styles.link}>Log in</a>
        </p>
      </div>
    </div>
  )
}

const styles = {
  container: {
    maxWidth: '400px',
    margin: '4rem auto',
    padding: '0 1rem',
  },
  card: {
    backgroundColor: 'white',
    borderRadius: '0.5rem',
    padding: '2rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  title: {
    fontSize: '1.875rem',
    fontWeight: 'bold',
    marginBottom: '0.5rem',
    textAlign: 'center' as const,
  },
  subtitle: {
    color: '#6b7280',
    textAlign: 'center' as const,
    marginBottom: '2rem',
  },
  success: {
    backgroundColor: '#d1fae5',
    color: '#065f46',
    padding: '0.75rem',
    borderRadius: '0.375rem',
    marginBottom: '1rem',
    fontSize: '0.875rem',
  },
  error: {
    backgroundColor: '#fee2e2',
    color: '#991b1b',
    padding: '0.75rem',
    borderRadius: '0.375rem',
    marginBottom: '1rem',
    fontSize: '0.875rem',
  },
  form: {
    marginBottom: '1.5rem',
  },
  input: {
    width: '100%',
    padding: '0.75rem',
    border: '1px solid #d1d5db',
    borderRadius: '0.375rem',
    fontSize: '1rem',
    marginBottom: '1rem',
  },
  button: {
    width: '100%',
    padding: '0.75rem',
    backgroundColor: '#2563eb',
    color: 'white',
    border: 'none',
    borderRadius: '0.375rem',
    fontSize: '1rem',
    fontWeight: 500,
  },
  divider: {
    textAlign: 'center' as const,
    color: '#9ca3af',
    margin: '1.5rem 0',
    position: 'relative' as const,
  },
  googleButton: {
    width: '100%',
    padding: '0.75rem',
    backgroundColor: 'white',
    color: '#1f2937',
    border: '1px solid #d1d5db',
    borderRadius: '0.375rem',
    fontSize: '1rem',
    fontWeight: 500,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
  },
  googleIcon: {
    fontWeight: 'bold',
    color: '#4285f4',
  },
  footer: {
    textAlign: 'center' as const,
    marginTop: '1.5rem',
    fontSize: '0.875rem',
    color: '#6b7280',
  },
  link: {
    color: '#2563eb',
    textDecoration: 'underline',
  },
}
