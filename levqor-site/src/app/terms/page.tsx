export const metadata = {
  title: 'Terms of Service — Levqor',
  description: 'Levqor terms of service and user agreement.',
}

export default function Terms() {
  return (
    <main style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <nav style={{ marginBottom: '4rem' }}>
        <a href="/" style={{ color: '#fff', textDecoration: 'none', fontSize: '1.5rem', fontWeight: 'bold' }}>← Levqor</a>
      </nav>

      <h1 style={{ fontSize: '3rem', marginBottom: '2rem' }}>Terms of Service</h1>

      <div style={{ lineHeight: 1.8, color: '#ccc' }}>
        <p style={{ marginBottom: '1.5rem' }}>Last updated: November 6, 2025</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Acceptance of Terms</h2>
        <p>By accessing and using Levqor, you accept and agree to be bound by these Terms of Service.</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Service Description</h2>
        <p>Levqor provides AI-powered business automation services. We reserve the right to modify, suspend, or discontinue any part of the service at any time.</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>User Responsibilities</h2>
        <p>You agree to:</p>
        <ul style={{ marginLeft: '1.5rem', marginBottom: '1.5rem' }}>
          <li>Provide accurate account information</li>
          <li>Maintain the security of your account credentials</li>
          <li>Use the service in compliance with applicable laws</li>
          <li>Not abuse, harm, or interfere with the service</li>
        </ul>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Free Tier</h2>
        <p>Free tier accounts receive 50 credits upon signup. Credits are consumed by automation runs. Additional credits can be purchased.</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Billing</h2>
        <p>Paid services are billed in advance. Refunds are handled on a case-by-case basis. You can cancel your subscription at any time.</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Limitation of Liability</h2>
        <p>Levqor is provided "as is" without warranties of any kind. We are not liable for any damages arising from your use of the service.</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Termination</h2>
        <p>We reserve the right to terminate or suspend accounts that violate these terms.</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Contact</h2>
        <p>For questions about these terms: <a href="mailto:legal@levqor.ai" style={{ color: '#fff' }}>legal@levqor.ai</a></p>
      </div>

      <footer style={{
        borderTop: '1px solid #333',
        paddingTop: '2rem',
        marginTop: '4rem',
        textAlign: 'center',
        color: '#666',
        fontSize: '0.875rem'
      }}>
        <div>
          <a href="/privacy" style={{ color: '#666', margin: '0 1rem' }}>Privacy</a>
          <a href="/contact" style={{ color: '#666', margin: '0 1rem' }}>Contact</a>
        </div>
      </footer>
    </main>
  )
}
