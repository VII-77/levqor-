export const metadata = {
  title: 'Contact Us — Levqor',
  description: 'Get in touch with the Levqor team for support, partnerships, or questions.',
}

export default function Contact() {
  return (
    <main style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <nav style={{ marginBottom: '4rem' }}>
        <a href="/" style={{ color: '#fff', textDecoration: 'none', fontSize: '1.5rem', fontWeight: 'bold' }}>← Levqor</a>
      </nav>

      <h1 style={{ fontSize: '3rem', marginBottom: '2rem' }}>Contact Us</h1>

      <div style={{ marginBottom: '3rem', lineHeight: 1.8, color: '#ccc' }}>
        <p>We'd love to hear from you. Reach out for support, partnerships, or general inquiries.</p>
      </div>

      <div style={{
        backgroundColor: '#111',
        padding: '2rem',
        borderRadius: '12px',
        border: '1px solid #333'
      }}>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Get in Touch</h2>
        <div style={{ marginBottom: '1rem' }}>
          <strong>Email:</strong> <a href="mailto:hello@levqor.ai" style={{ color: '#fff' }}>hello@levqor.ai</a>
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <strong>Support:</strong> <a href="mailto:support@levqor.ai" style={{ color: '#fff' }}>support@levqor.ai</a>
        </div>
        <div>
          <strong>Partnerships:</strong> <a href="mailto:partnerships@levqor.ai" style={{ color: '#fff' }}>partnerships@levqor.ai</a>
        </div>
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
          <a href="/terms" style={{ color: '#666', margin: '0 1rem' }}>Terms</a>
        </div>
      </footer>
    </main>
  )
}
