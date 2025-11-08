'use client';

import { useEffect, useState } from 'react';

export default function StatusPill() {
  const [status, setStatus] = useState<'pass' | 'fail' | 'loading'>('loading');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const res = await fetch('https://api.levqor.ai/status');
        const data = await res.json();
        setStatus(data.status === 'pass' ? 'pass' : 'fail');
      } catch {
        setStatus('fail');
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium bg-white/10 backdrop-blur-sm border border-white/20">
      <span
        className={`w-2 h-2 rounded-full ${
          status === 'pass' ? 'bg-green-400' : status === 'fail' ? 'bg-red-400' : 'bg-yellow-400'
        }`}
      />
      <span className="text-white">
        {status === 'pass' ? 'All Systems Operational' : status === 'fail' ? 'Degraded' : 'Checking...'}
      </span>
    </div>
  );
}
