'use client';

import { useEffect, useState } from 'react';

interface Metrics {
  health?: any;
  uptime?: any;
  queueHealth?: any;
}

export default function AdminInsightsPage() {
  const [metrics, setMetrics] = useState<Metrics>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const [healthRes, uptimeRes, queueRes] = await Promise.all([
          fetch('/api/health'),
          fetch('/api/ops/uptime'),
          fetch('/api/ops/queue_health')
        ]);

        const data: Metrics = {};

        if (healthRes.ok) {
          data.health = await healthRes.json();
        }

        if (uptimeRes.ok) {
          data.uptime = await uptimeRes.json();
        }

        if (queueRes.ok) {
          data.queueHealth = await queueRes.json();
        }

        setMetrics(data);
      } catch (err) {
        setError('Failed to fetch metrics');
        console.error('Error fetching metrics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  const formatUptime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}h ${minutes}m ${secs}s`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
            <div className="grid gap-6 md:grid-cols-3">
              {[1, 2, 3].map(i => (
                <div key={i} className="bg-white rounded-lg shadow p-6">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                  <div className="space-y-2">
                    <div className="h-4 bg-gray-200 rounded"></div>
                    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Intelligence Panel</h1>
          <p className="mt-2 text-sm text-gray-600">
            Advanced system metrics, AI insights, and operational intelligence
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-3 mb-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">System Health</h2>
            <div className="space-y-3">
              {metrics.health ? (
                <>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Status</span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      metrics.health.status === 'pass'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {metrics.health.status}
                    </span>
                  </div>
                  {metrics.health.checks && (
                    <div className="text-xs text-gray-500 mt-2">
                      <div className="font-medium">Components:</div>
                      {Object.entries(metrics.health.checks).map(([key, value]: [string, any]) => (
                        <div key={key} className="flex justify-between mt-1">
                          <span>{key}</span>
                          <span className={value.status === 'pass' ? 'text-green-600' : 'text-red-600'}>
                            {value.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <p className="text-sm text-gray-500">No data</p>
              )}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Uptime</h2>
            <div className="space-y-3">
              {metrics.uptime ? (
                <>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Running</span>
                    <span className="text-sm font-medium text-gray-900">
                      {formatUptime(metrics.uptime.uptime_seconds)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Version</span>
                    <span className="text-sm font-medium text-gray-900">
                      {metrics.uptime.version}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Build</span>
                    <span className="text-sm font-medium text-gray-900">
                      {metrics.uptime.build}
                    </span>
                  </div>
                </>
              ) : (
                <p className="text-sm text-gray-500">No data</p>
              )}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Queue Health</h2>
            <div className="space-y-3">
              {metrics.queueHealth ? (
                <>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Status</span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      metrics.queueHealth.queue_status === 'healthy'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {metrics.queueHealth.queue_status}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Pending Jobs</span>
                    <span className="text-sm font-medium text-gray-900">
                      {metrics.queueHealth.pending_jobs || 0}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Completed</span>
                    <span className="text-sm font-medium text-gray-900">
                      {metrics.queueHealth.completed_jobs || 0}
                    </span>
                  </div>
                </>
              ) : (
                <p className="text-sm text-gray-500">No data</p>
              )}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Intelligence Features</h2>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-medium text-gray-900 mb-2">Anomaly Detection</h3>
              <p className="text-sm text-gray-600">
                Statistical latency monitoring using Z-score and IQR methods for early issue detection.
              </p>
            </div>
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-medium text-gray-900 mb-2">Adaptive Pricing</h3>
              <p className="text-sm text-gray-600">
                Usage-aware pricing model with load factors and performance bonuses.
              </p>
            </div>
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-medium text-gray-900 mb-2">Smart Alerts</h3>
              <p className="text-sm text-gray-600">
                Multi-channel notification system (Slack, Telegram, Email) for critical events.
              </p>
            </div>
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-medium text-gray-900 mb-2">Auto-Tuning</h3>
              <p className="text-sm text-gray-600">
                SLO and p95 target optimization for continuous performance improvement.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>Admin Panel:</strong> This dashboard provides advanced operational intelligence 
            powered by v6.5 AI features including anomaly detection, adaptive pricing, and automated 
            governance reporting.
          </p>
        </div>
      </div>
    </div>
  );
}
