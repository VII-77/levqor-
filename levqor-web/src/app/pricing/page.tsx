import { Metadata } from 'next';
import CTAButton from '@/components/CTAButton';

export const metadata: Metadata = {
  title: 'Pricing - Levqor',
  description: 'Simple, transparent pricing for Levqor job orchestration. Start free, scale when ready.',
  alternates: {
    canonical: 'https://app.levqor.ai/pricing',
  },
  openGraph: {
    title: 'Pricing - Levqor',
    description: 'Simple, transparent pricing for Levqor job orchestration. Start free, scale when ready.',
    type: 'website',
    url: 'https://app.levqor.ai/pricing',
    images: [
      {
        url: '/og/pricing.jpg',
        width: 1200,
        height: 630,
        alt: 'Levqor Pricing',
      },
    ],
  },
};

export default function Pricing() {
  const plans = [
    {
      name: 'Test Plan',
      price: '$1',
      period: 'one-time',
      plan: 'test' as const,
      features: [
        'Test all features',
        'Limited to 10 API calls',
        'Valid for 7 days',
        'Email support',
      ],
    },
    {
      name: 'Monthly',
      price: '$19',
      period: 'per month',
      plan: 'monthly' as const,
      features: [
        '10,000 API calls/month',
        'All connectors included',
        'Priority support',
        'Advanced analytics',
        'Custom workflows',
      ],
      popular: true,
    },
    {
      name: 'Annual',
      price: '$190',
      period: 'per year',
      plan: 'annual' as const,
      features: [
        '120,000 API calls/year',
        'All connectors included',
        '24/7 priority support',
        'Advanced analytics',
        'Custom workflows',
        'Dedicated account manager',
        'Save $38 per year',
      ],
    },
  ];

  return (
    <main style={{
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '40px 20px',
    }}>
      <section style={{
        textAlign: 'center',
        marginBottom: '60px',
      }}>
        <h1 style={{
          fontSize: '48px',
          fontWeight: 700,
          marginBottom: '16px',
        }}>
          Simple, Transparent Pricing
        </h1>
        <p style={{
          fontSize: '20px',
          color: '#666',
          maxWidth: '600px',
          margin: '0 auto',
        }}>
          Choose the plan that fits your needs. All plans include our core features.
        </p>
      </section>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '32px',
        marginBottom: '60px',
      }}>
        {plans.map((plan) => (
          <div
            key={plan.name}
            style={{
              padding: '32px',
              border: plan.popular ? '2px solid #0066cc' : '1px solid #e0e0e0',
              borderRadius: '12px',
              backgroundColor: '#fff',
              position: 'relative',
            }}
          >
            {plan.popular && (
              <div style={{
                position: 'absolute',
                top: '-12px',
                left: '50%',
                transform: 'translateX(-50%)',
                padding: '4px 12px',
                backgroundColor: '#0066cc',
                color: '#fff',
                fontSize: '12px',
                fontWeight: 600,
                borderRadius: '12px',
              }}>
                MOST POPULAR
              </div>
            )}
            <h3 style={{
              fontSize: '24px',
              fontWeight: 600,
              marginBottom: '16px',
            }}>
              {plan.name}
            </h3>
            <div style={{ marginBottom: '24px' }}>
              <span style={{
                fontSize: '48px',
                fontWeight: 700,
                color: '#0066cc',
              }}>
                {plan.price}
              </span>
              <span style={{
                fontSize: '16px',
                color: '#666',
                marginLeft: '8px',
              }}>
                {plan.period}
              </span>
            </div>
            <ul style={{
              listStyle: 'none',
              padding: 0,
              marginBottom: '32px',
            }}>
              {plan.features.map((feature, index) => (
                <li
                  key={index}
                  style={{
                    padding: '12px 0',
                    borderBottom: '1px solid #f0f0f0',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                  }}
                >
                  <span style={{ color: '#2e7d32', fontWeight: 600 }}>✓</span>
                  {feature}
                </li>
              ))}
            </ul>
            <CTAButton plan={plan.plan}>
              Get Started
            </CTAButton>
          </div>
        ))}
      </div>

      <div style={{
        textAlign: 'center',
        padding: '40px 20px',
        backgroundColor: '#f9f9f9',
        borderRadius: '8px',
      }}>
        <h2 style={{
          fontSize: '32px',
          fontWeight: 600,
          marginBottom: '16px',
        }}>
          Questions about pricing?
        </h2>
        <p style={{
          fontSize: '18px',
          color: '#666',
          marginBottom: '24px',
        }}>
          Contact our sales team for custom enterprise solutions.
        </p>
        <a
          href="mailto:sales@levqor.ai"
          style={{
            display: 'inline-block',
            padding: '12px 24px',
            fontSize: '16px',
            fontWeight: 600,
            color: '#0066cc',
            textDecoration: 'none',
            border: '2px solid #0066cc',
            borderRadius: '6px',
          }}
        >
          Contact Sales
        </a>
      </div>
    </main>
  );
}
