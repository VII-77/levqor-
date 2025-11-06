import { redirect } from 'next/navigation';

interface MetricsSummary {
  total: {
    page_views: number;
    cta_clicks: number;
    newsletters: number;
    conversions: number;
  };
  last_24h: {
    page_views: number;
    cta_clicks: number;
  };
  last_7d: {
    page_views: number;
  };
  by_day: Record<string, Record<string, number>>;
  conversion_rate: number;
  cta_rate: number;
  last_updated: number;
}

interface MarketingSummary {
  visits: number;
  conversions: number;
  mrr: number;
  active_users: number;
  jobs_processed_total: number;
  uptime_7d: number;
}

async function getMetricsSummary(): Promise<MetricsSummary | null> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_BASE}/api/v1/metrics/summary`, {
      cache: 'no-store',
    });
    
    if (!res.ok) return null;
    return res.json();
  } catch (error) {
    console.error('Failed to fetch metrics:', error);
    return null;
  }
}

async function getMarketingSummary(): Promise<MarketingSummary | null> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_BASE}/api/v1/marketing/summary`, {
      cache: 'no-store',
    });
    
    if (!res.ok) return null;
    return res.json();
  } catch (error) {
    console.error('Failed to fetch marketing summary:', error);
    return null;
  }
}

export default async function DashboardPage({
  searchParams,
}: {
  searchParams: { token?: string };
}) {
  const token = searchParams.token;
  
  const validToken = process.env.DASHBOARD_TOKEN || 'test';
  
  if (!token || token !== validToken) {
    return (
      <main style={{
        maxWidth: '600px',
        margin: '100px auto',
        padding: '40px',
        textAlign: 'center',
        backgroundColor: '#fff',
        borderRadius: '8px',
        border: '1px solid #e0e0e0',
      }}>
        <h1 style={{ fontSize: '48px', marginBottom: '16px' }}>403</h1>
        <h2 style={{ fontSize: '24px', fontWeight: 600, marginBottom: '16px' }}>
          Access Denied
        </h2>
        <p style={{ color: '#666', marginBottom: '24px' }}>
          Valid authentication token required to access this dashboard.
        </p>
        <a
          href="/"
          style={{
            display: 'inline-block',
            padding: '12px 24px',
            backgroundColor: '#0066cc',
            color: '#fff',
            textDecoration: 'none',
            borderRadius: '6px',
            fontWeight: 600,
          }}
        >
          Back to Home
        </a>
      </main>
    );
  }

  const [metrics, marketing] = await Promise.all([
    getMetricsSummary(),
    getMarketingSummary(),
  ]);

  if (!metrics) {
    return (
      <main style={{ maxWidth: '1200px', margin: '40px auto', padding: '20px' }}>
        <h1>Analytics Dashboard</h1>
        <p style={{ color: '#d32f2f', marginTop: '20px' }}>
          Failed to load metrics data. Please check backend connectivity.
        </p>
      </main>
    );
  }

  return (
    <main style={{
      maxWidth: '1200px',
      margin: '40px auto',
      padding: '20px',
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '40px',
      }}>
        <h1 style={{ fontSize: '36px', fontWeight: 700 }}>
          Analytics Dashboard
        </h1>
        <a
          href="/"
          style={{
            padding: '8px 16px',
            color: '#0066cc',
            textDecoration: 'none',
            border: '1px solid #0066cc',
            borderRadius: '6px',
          }}
        >
          Back to Home
        </a>
      </div>

      <section style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '24px', fontWeight: 600, marginBottom: '20px' }}>
          Overview
        </h2>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '20px',
        }}>
          <StatCard
            label="Total Page Views"
            value={metrics.total.page_views.toLocaleString()}
            subtitle={`${metrics.last_24h.page_views} in last 24h`}
          />
          <StatCard
            label="CTA Clicks"
            value={metrics.total.cta_clicks.toLocaleString()}
            subtitle={`${metrics.last_24h.cta_clicks} in last 24h`}
          />
          <StatCard
            label="Newsletter Signups"
            value={metrics.total.newsletters.toLocaleString()}
            subtitle="Total subscriptions"
          />
          <StatCard
            label="Conversions"
            value={metrics.total.conversions.toLocaleString()}
            subtitle={`${metrics.conversion_rate}% conversion rate`}
          />
        </div>
      </section>

      <section style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '24px', fontWeight: 600, marginBottom: '20px' }}>
          Performance Metrics
        </h2>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '20px',
        }}>
          <StatCard
            label="CTR (Click-Through Rate)"
            value={`${metrics.cta_rate}%`}
            subtitle="CTA clicks / page views"
          />
          <StatCard
            label="Conversion Rate"
            value={`${metrics.conversion_rate}%`}
            subtitle="Conversions / page views"
          />
          {marketing && (
            <>
              <StatCard
                label="Active Users"
                value={marketing.active_users.toLocaleString()}
                subtitle="Monthly active"
              />
              <StatCard
                label="MRR"
                value={`$${marketing.mrr.toLocaleString()}`}
                subtitle="Monthly recurring revenue"
              />
            </>
          )}
        </div>
      </section>

      <section style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '24px', fontWeight: 600, marginBottom: '20px' }}>
          7-Day Activity
        </h2>
        <div style={{
          backgroundColor: '#f9f9f9',
          padding: '20px',
          borderRadius: '8px',
        }}>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
          }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #e0e0e0' }}>
                <th style={{ padding: '12px', textAlign: 'left' }}>Date</th>
                <th style={{ padding: '12px', textAlign: 'right' }}>Page Views</th>
                <th style={{ padding: '12px', textAlign: 'right' }}>CTA Clicks</th>
                <th style={{ padding: '12px', textAlign: 'right' }}>Newsletters</th>
                <th style={{ padding: '12px', textAlign: 'right' }}>Conversions</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(metrics.by_day)
                .sort(([a], [b]) => b.localeCompare(a))
                .map(([day, events]) => (
                  <tr key={day} style={{ borderBottom: '1px solid #e0e0e0' }}>
                    <td style={{ padding: '12px' }}>{day}</td>
                    <td style={{ padding: '12px', textAlign: 'right' }}>
                      {events.page_view || 0}
                    </td>
                    <td style={{ padding: '12px', textAlign: 'right' }}>
                      {events.cta_click || 0}
                    </td>
                    <td style={{ padding: '12px', textAlign: 'right' }}>
                      {events.newsletter || 0}
                    </td>
                    <td style={{ padding: '12px', textAlign: 'right' }}>
                      {events.conversion || 0}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </section>

      <footer style={{
        marginTop: '60px',
        paddingTop: '20px',
        borderTop: '1px solid #e0e0e0',
        textAlign: 'center',
        color: '#666',
        fontSize: '14px',
      }}>
        Last updated: {new Date(metrics.last_updated * 1000).toLocaleString()}
      </footer>
    </main>
  );
}

function StatCard({
  label,
  value,
  subtitle,
}: {
  label: string;
  value: string;
  subtitle?: string;
}) {
  return (
    <div style={{
      padding: '24px',
      backgroundColor: '#fff',
      border: '1px solid #e0e0e0',
      borderRadius: '8px',
    }}>
      <div style={{
        fontSize: '14px',
        color: '#666',
        marginBottom: '8px',
        fontWeight: 500,
      }}>
        {label}
      </div>
      <div style={{
        fontSize: '32px',
        fontWeight: 700,
        color: '#0066cc',
        marginBottom: '4px',
      }}>
        {value}
      </div>
      {subtitle && (
        <div style={{
          fontSize: '12px',
          color: '#999',
        }}>
          {subtitle}
        </div>
      )}
    </div>
  );
}
