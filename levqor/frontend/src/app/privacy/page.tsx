export default function PrivacyPage() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Privacy Policy</h1>
      <div style={styles.content}>
        <p>Last updated: November 6, 2025</p>
        
        <h2 style={styles.heading}>Information We Collect</h2>
        <p>
          We collect information you provide directly to us, such as when you create an account,
          use our services, or communicate with us. This may include your email address,
          usage data, and automation configurations.
        </p>

        <h2 style={styles.heading}>How We Use Your Information</h2>
        <p>
          We use the information we collect to provide, maintain, and improve our services,
          to communicate with you, and to monitor and analyze trends and usage.
        </p>

        <h2 style={styles.heading}>Data Security</h2>
        <p>
          We implement appropriate technical and organizational measures to protect your
          personal information against unauthorized access, alteration, disclosure, or destruction.
        </p>

        <h2 style={styles.heading}>Contact Us</h2>
        <p>
          If you have any questions about this Privacy Policy, please contact us at{' '}
          <a href="mailto:privacy@levqor.ai" style={styles.link}>privacy@levqor.ai</a>
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
