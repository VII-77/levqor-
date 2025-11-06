export const metadata = {
  title: 'Privacy Policy — Levqor',
  description: 'Levqor privacy policy and data handling practices.',
}

export default function Privacy() {
  return (
    <main style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <nav style={{ marginBottom: '4rem' }}>
        <a href="/" style={{ color: '#fff', textDecoration: 'none', fontSize: '1.5rem', fontWeight: 'bold' }}>← Levqor</a>
      </nav>

      <h1 style={{ fontSize: '3rem', marginBottom: '2rem' }}>Privacy Policy</h1>

      <div style={{ lineHeight: 1.8, color: '#ccc' }}>
        <p style={{ marginBottom: '1.5rem' }}>Last updated: November 6, 2025</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Data We Collect</h2>
        <p>We collect only the data necessary to provide our automation services:</p>
        <ul style={{ marginLeft: '1.5rem', marginBottom: '1.5rem' }}>
          <li>Email address for account creation and notifications</li>
          <li>Usage data for service improvement and analytics</li>
          <li>Integration credentials (stored encrypted) for connected services</li>
        </ul>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>How We Use Your Data</h2>
        <p>Your data is used to:</p>
        <ul style={{ marginLeft: '1.5rem', marginBottom: '1.5rem' }}>
          <li>Provide and improve our automation services</li>
          <li>Send service-related communications</li>
          <li>Analyze usage patterns to enhance features</li>
        </ul>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Data Security</h2>
        <p>We implement industry-standard security measures including encryption at rest and in transit, regular security audits, and strict access controls.</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Your Rights</h2>
        <p>You have the right to access, modify, or delete your data at any time. Contact us at <a href="mailto:privacy@levqor.ai" style={{ color: '#fff' }}>privacy@levqor.ai</a> for data requests.</p>

        <h2 style={{ fontSize: '1.5rem', color: '#fff', marginTop: '2rem', marginBottom: '1rem' }}>Contact</h2>
        <p>For privacy concerns: <a href="mailto:privacy@levqor.ai" style={{ color: '#fff' }}>privacy@levqor.ai</a></p>
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
          <a href="/terms" style={{ color: '#666', margin: '0 1rem' }}>Terms</a>
          <a href="/contact" style={{ color: '#666', margin: '0 1rem' }}>Contact</a>
        </div>
      </footer>
    </main>
  )
}
