import CTAButton from '@/components/CTAButton';
import USPGrid from '@/components/USPGrid';
import Testimonials from '@/components/Testimonials';
import LiveStats from '@/components/LiveStats';
import SubscribeForm from '@/components/SubscribeForm';
import Link from 'next/link';

interface LandingData {
  headline: string;
  subheadline: string;
  cta_primary: string;
  cta_secondary: string;
}

async function getLandingData(): Promise<LandingData> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_ASSETS_BASE}/marketing/landing_snippets.json`, {
      cache: 'no-store',
    });
    
    if (!res.ok) {
      throw new Error('Failed to fetch landing data');
    }
    
    return res.json();
  } catch (error) {
    return {
      headline: 'Production-Ready Job Orchestration for AI Automation',
      subheadline: 'Stop rebuilding infrastructure. Start building AI features.',
      cta_primary: 'Start Free Trial',
      cta_secondary: 'View Documentation',
    };
  }
}

export default async function Home() {
  const data = await getLandingData();

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
        <h1 style={{
          fontSize: '48px',
          fontWeight: 700,
          marginBottom: '24px',
          lineHeight: 1.2,
        }}>
          {data.headline}
        </h1>
        <p style={{
          fontSize: '24px',
          color: '#666',
          marginBottom: '40px',
          maxWidth: '700px',
          margin: '0 auto 40px',
        }}>
          {data.subheadline}
        </p>
        <div style={{
          display: 'flex',
          gap: '16px',
          justifyContent: 'center',
          flexWrap: 'wrap',
        }}>
          <CTAButton plan="monthly">
            {data.cta_primary}
          </CTAButton>
          <Link href="/pricing">
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
              {data.cta_secondary}
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
