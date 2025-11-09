'use client';

import { useEffect, useState } from 'react';

interface SystemHealth {
  status: string;
  uptime_seconds?: number;
  version?: string;
}

export default function InsightsPage() {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [uptime, setUptime] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [healthRes, uptimeRes] = await Promise.all([
          fetch('/api/status'),
          fetch('/api/ops/uptime')
        ]);

        if (healthRes.ok) {
          const healthData = await healthRes.json();
          setHealth(healthData);
        }

        if (uptimeRes.ok) {
          const uptimeData = await uptimeRes.json();
          setUptime(uptimeData);
        }
      } catch (error) {
        console.error('Failed to fetch insights:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formatUptime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Operational Insights</h1>
          <p className="mt-2 text-sm text-gray-600">
            Real-time system health and performance metrics
          </p>
        </div>

        {loading ? (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="animate-pulse flex space-x-4">
              <div className="flex-1 space-y-4 py-1">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="space-y-2">
                  <div className="h-4 bg-gray-200 rounded"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">System Status</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Status</span>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    health?.status === 'pass' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {health?.status || 'Unknown'}
                  </span>
                </div>
                {uptime && (
                  <>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Uptime</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatUptime(uptime.uptime_seconds)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Version</span>
                      <span className="text-sm font-medium text-gray-900">
                        {uptime.version}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Build</span>
                      <span className="text-sm font-medium text-gray-900">
                        {uptime.build}
                      </span>
                    </div>
                  </>
                )}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">API Endpoint</span>
                  <span className="text-xs font-mono text-gray-900">
                    api.levqor.ai
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Environment</span>
                  <span className="text-sm font-medium text-gray-900">
                    Production
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Region</span>
                  <span className="text-sm font-medium text-gray-900">
                    Global
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>Note:</strong> This dashboard displays real-time operational metrics 
            from the Levqor API. More advanced analytics and AI insights are available 
            in the admin panel.
          </p>
        </div>
      </div>
    </div>
  );
}
