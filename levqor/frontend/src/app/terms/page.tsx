export default function TermsPage() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Terms of Service</h1>
      <div style={styles.content}>
        <p>Last updated: November 6, 2025</p>
        
        <h2 style={styles.heading}>Acceptance of Terms</h2>
        <p>
          By accessing and using Levqor, you accept and agree to be bound by the terms
          and provisions of this agreement.
        </p>

        <h2 style={styles.heading}>Use of Service</h2>
        <p>
          You agree to use the service only for lawful purposes and in accordance with
          these Terms. You must not use our service in any way that violates any applicable
          federal, state, local, or international law or regulation.
        </p>

        <h2 style={styles.heading}>Credits and Billing</h2>
        <p>
          Each automation run costs 1 credit. Credits are non-refundable but never expire.
          You can purchase credit packs at any time. Free credits are provided as a
          promotional offer and may be adjusted or discontinued.
        </p>

        <h2 style={styles.heading}>Termination</h2>
        <p>
          We may terminate or suspend your account and access to the service immediately,
          without prior notice or liability, for any reason, including breach of these Terms.
        </p>

        <h2 style={styles.heading}>Contact</h2>
        <p>
          Questions about the Terms of Service should be sent to{' '}
          <a href="mailto:legal@levqor.ai" style={styles.link}>legal@levqor.ai</a>
        </p>
      </div>
    </div>
  )
}

const styles = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '2rem 1rem',
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: 'bold',
    marginBottom: '2rem',
  },
  content: {
    lineHeight: 1.7,
    color: '#4b5563',
  },
  heading: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    marginTop: '2rem',
    marginBottom: '1rem',
    color: '#111827',
  },
  link: {
    color: '#2563eb',
    textDecoration: 'underline',
  },
}
