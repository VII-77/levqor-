'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    setError('')

    try {
      const { error } = await supabase.auth.signInWithOtp({
        email,
        options: {
          emailRedirectTo: `${window.location.origin}/dashboard`
        }
      })

      if (error) throw error

      setMessage('Check your email for the magic link!')
    } catch (err: any) {
      setError(err.message || 'Failed to send login link')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Log In to Levqor</h1>

        {message && (
          <div style={styles.success}>{message}</div>
        )}

        {error && (
          <div style={styles.error}>{error}</div>
        )}

        <form onSubmit={handleLogin} style={styles.form}>
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

        <p style={styles.footer}>
          Don't have an account? <a href="/signup" style={styles.link}>Sign up</a>
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
    marginBottom: '2rem',
    textAlign: 'center' as const,
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
