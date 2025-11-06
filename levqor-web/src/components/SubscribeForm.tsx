'use client';

import { useState, FormEvent } from 'react';
import { logEvent } from '@/utils/metrics';

export default function SubscribeForm() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    setMessage('');

    logEvent('newsletter', { email_hash: btoa(email).substring(0, 16) });

    try {
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_BASE;
      
      if (backendUrl) {
        const response = await fetch(`${backendUrl}/api/v1/newsletter/subscribe`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email }),
        });

        if (response.ok) {
          setStatus('success');
          setMessage('Thanks! Check your email to confirm your subscription.');
          setEmail('');
        } else {
          throw new Error('Subscription failed');
        }
      } else {
        if (typeof window !== 'undefined') {
          localStorage.setItem('levqor_newsletter_email', JSON.stringify({
            email,
            timestamp: Date.now(),
          }));
        }
        setStatus('success');
        setMessage("We'll confirm by email.");
        setEmail('');
      }
    } catch (error) {
      setStatus('error');
      setMessage('Something went wrong. Please try again.');
    }
  };

  return (
    <div style={{
      maxWidth: '500px',
      margin: '40px auto',
      padding: '32px',
      backgroundColor: '#f9f9f9',
      borderRadius: '8px',
    }}>
      <h3 style={{
        fontSize: '24px',
        fontWeight: 600,
        marginBottom: '12px',
        textAlign: 'center',
      }}>
        Stay Updated
      </h3>
      <p style={{
        color: '#666',
        marginBottom: '24px',
        textAlign: 'center',
      }}>
        Get the latest updates on features and product news.
      </p>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '12px' }}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="your@email.com"
          required
          disabled={status === 'loading'}
          style={{
            flex: 1,
            padding: '12px',
            fontSize: '16px',
            border: '1px solid #ddd',
            borderRadius: '6px',
          }}
        />
        <button
          type="submit"
          disabled={status === 'loading'}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            fontWeight: 600,
            color: '#fff',
            backgroundColor: status === 'loading' ? '#999' : '#0066cc',
            border: 'none',
            borderRadius: '6px',
            cursor: status === 'loading' ? 'not-allowed' : 'pointer',
          }}
        >
          {status === 'loading' ? 'Sending...' : 'Subscribe'}
        </button>
      </form>
      {message && (
        <p style={{
          marginTop: '16px',
          textAlign: 'center',
          color: status === 'success' ? '#2e7d32' : '#d32f2f',
          fontSize: '14px',
        }}>
          {message}
        </p>
      )}
    </div>
  );
}
