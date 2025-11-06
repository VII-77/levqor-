import type { Metadata } from 'next';
import Script from 'next/script';
import './globals.css';
import RefCapture from '@/components/RefCapture';

export const metadata: Metadata = {
  title: 'Levqor - Production-Ready Job Orchestration for AI Automation',
  description: 'Levqor — autonomous ops. Stop rebuilding infrastructure. Start building AI features with enterprise-grade job orchestration.',
  openGraph: {
    title: 'Levqor - Production-Ready Job Orchestration for AI Automation',
    description: 'Levqor — autonomous ops. Enterprise-grade job orchestration API with built-in connectors, security, and monitoring.',
    type: 'website',
    url: 'https://levqor.com',
    siteName: 'Levqor',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Levqor - Job Orchestration Platform',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Levqor - Production-Ready Job Orchestration for AI Automation',
    description: 'Enterprise-grade job orchestration API with built-in connectors, security, and monitoring.',
    images: ['/og-image.jpg'],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const plausibleDomain = process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN;
  const heapId = process.env.NEXT_PUBLIC_HEAP_ID;

  return (
    <html lang="en">
      <head>
        {plausibleDomain && (
          <Script
            defer
            data-domain={plausibleDomain}
            src="https://plausible.io/js/script.js"
          />
        )}
        {heapId && (
          <Script id="heap-analytics">
            {`
              window.heap=window.heap||[],heap.load=function(e,t){window.heap.appid=e,window.heap.config=t=t||{};var r=document.createElement("script");r.type="text/javascript",r.async=!0,r.src="https://cdn.heapanalytics.com/js/heap-"+e+".js";var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(r,a);for(var n=function(e){return function(){heap.push([e].concat(Array.prototype.slice.call(arguments,0)))}},p=["addEventProperties","addUserProperties","clearEventProperties","identify","resetIdentity","removeEventProperty","setEventProperties","track","unsetEventProperty"],o=0;o<p.length;o++)heap[p[o]]=n(p[o])};
              heap.load("${heapId}");
            `}
          </Script>
        )}
      </head>
      <body>
        <RefCapture />
        <nav style={{
          borderBottom: '1px solid #e0e0e0',
          padding: '16px 20px',
        }}>
          <div style={{
            maxWidth: '1200px',
            margin: '0 auto',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
            <a href="/" style={{
              fontSize: '24px',
              fontWeight: 700,
              color: '#0066cc',
              textDecoration: 'none',
            }}>
              {process.env.NEXT_PUBLIC_APP_NAME || 'Levqor'}
            </a>
            <div style={{
              display: 'flex',
              gap: '24px',
              alignItems: 'center',
            }}>
              <a href="/" style={{
                color: '#333',
                textDecoration: 'none',
                fontWeight: 500,
              }}>
                Home
              </a>
              <a href="/pricing" style={{
                color: '#333',
                textDecoration: 'none',
                fontWeight: 500,
              }}>
                Pricing
              </a>
              <a href="https://api.levqor.ai/public/docs/" style={{
                color: '#333',
                textDecoration: 'none',
                fontWeight: 500,
              }}>
                Docs
              </a>
              <a href="https://api.levqor.ai/public/blog/" style={{
                color: '#333',
                textDecoration: 'none',
                fontWeight: 500,
              }}>
                Blog
              </a>
            </div>
          </div>
        </nav>
        {children}
        <footer style={{
          borderTop: '1px solid #e0e0e0',
          padding: '40px 20px',
          marginTop: '80px',
          textAlign: 'center',
          color: '#666',
        }}>
          <p>&copy; 2025 Levqor. All rights reserved.</p>
        </footer>
      </body>
    </html>
  );
}
