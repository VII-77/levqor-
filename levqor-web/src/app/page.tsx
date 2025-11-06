import CTAButton from '@/components/CTAButton';
import USPGrid from '@/components/USPGrid';
import Testimonials from '@/components/Testimonials';
import LiveStats from '@/components/LiveStats';
import SubscribeForm from '@/components/SubscribeForm';
import StatusBadge from '@/components/StatusBadge';
import Link from 'next/link';

export default function Home() {
  return (
    <main style={{
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '40px 20px',
    }}>
      <section style={{
        textAlign: 'center',
        padding: '80px 20px',
      }}>
        <StatusBadge />
        <h1 style={{
          fontSize: '48px',
          fontWeight: 700,
          marginBottom: '24px',
          lineHeight: 1.2,
        }}>
          Levqor automates your business with a self-running AI engine
        </h1>
        <p style={{
          fontSize: '24px',
          color: '#666',
          marginBottom: '40px',
          maxWidth: '700px',
          margin: '0 auto 40px',
        }}>
          No cron. No plugins.
        </p>
        <div style={{
          display: 'flex',
          gap: '16px',
          justifyContent: 'center',
          flexWrap: 'wrap',
        }}>
          <Link href="/pricing">
            <button style={{
              padding: '14px 28px',
              fontSize: '16px',
              fontWeight: 600,
              color: '#fff',
              backgroundColor: '#0066cc',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
            }}>
              View Pricing
            </button>
          </Link>
          <Link href="https://api.levqor.ai/public/docs/" target="_blank">
            <button style={{
              padding: '12px 24px',
              fontSize: '16px',
              fontWeight: 600,
              color: '#0066cc',
              backgroundColor: '#fff',
              border: '2px solid #0066cc',
              borderRadius: '6px',
              cursor: 'pointer',
            }}>
              View Documentation
            </button>
          </Link>
        </div>
      </section>

      <LiveStats />

      <USPGrid />

      <Testimonials />

      <SubscribeForm />
    </main>
  );
}
