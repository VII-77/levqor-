'use client';

import { useEffect, useState } from 'react';

export default function StatusBadge() {
  const [status, setStatus] = useState<'operational' | 'degraded' | 'down' | 'loading'>('loading');
  const statusUrl = process.env.NEXT_PUBLIC_STATUS_URL;

  useEffect(() => {
    if (!statusUrl) {
      setStatus('operational');
      return;
    }

    const checkStatus = async () => {
      try {
        const response = await fetch(statusUrl, { cache: 'no-store' });
        if (response.ok) {
          const data = await response.json();
          setStatus(data.status === 'healthy' ? 'operational' : 'degraded');
        } else {
          setStatus('degraded');
        }
      } catch {
        setStatus('degraded');
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 60000); // Check every minute
    return () => clearInterval(interval);
  }, [statusUrl]);

  const statusConfig = {
    operational: { color: '#4caf50', text: '● All Systems Operational', bg: '#e8f5e9' },
    degraded: { color: '#ff9800', text: '● Degraded Performance', bg: '#fff3e0' },
    down: { color: '#d32f2f', text: '● System Down', bg: '#ffebee' },
    loading: { color: '#999', text: '● Checking Status...', bg: '#f5f5f5' },
  };

  const config = statusConfig[status];

  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '6px 14px',
        backgroundColor: config.bg,
        borderRadius: '20px',
        fontSize: '13px',
        fontWeight: 500,
        color: config.color,
        marginBottom: '16px',
      }}
    >
      {config.text}
    </div>
  );
}
