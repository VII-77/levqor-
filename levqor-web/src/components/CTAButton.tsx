'use client';

import { useState } from 'react';
import { logEvent } from '@/utils/metrics';

interface CTAButtonProps {
  plan?: 'monthly' | 'annual' | 'test';
  children?: React.ReactNode;
}

export default function CTAButton({ plan = 'monthly', children }: CTAButtonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleClick = async () => {
    setLoading(true);
    setError(null);

    logEvent('cta_click', { plan });

    try {
      const response = await fetch(process.env.NEXT_PUBLIC_BACKEND_CHECKOUT || '', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ plan }),
      });

      if (!response.ok) {
        throw new Error(`Checkout failed: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.url) {
        window.location.href = data.url;
      } else {
        throw new Error('No checkout URL returned');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start checkout');
      setLoading(false);
    }
  };

  return (
    <div>
      <button
        onClick={handleClick}
        disabled={loading}
        className="cta-button"
        style={{
          padding: '12px 24px',
          fontSize: '16px',
          fontWeight: 600,
          color: '#fff',
          backgroundColor: loading ? '#999' : '#0066cc',
          border: 'none',
          borderRadius: '6px',
          cursor: loading ? 'not-allowed' : 'pointer',
          transition: 'background-color 0.2s',
        }}
        onMouseOver={(e) => !loading && (e.currentTarget.style.backgroundColor = '#0052a3')}
        onMouseOut={(e) => !loading && (e.currentTarget.style.backgroundColor = '#0066cc')}
      >
        {loading ? 'Loading...' : children || 'Start Free Trial'}
      </button>
      {error && <p style={{ color: '#d32f2f', marginTop: '8px', fontSize: '14px' }}>{error}</p>}
    </div>
  );
}
