export default function Home() {
  return (
    <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      <nav style={{ marginBottom: '4rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Levqor</div>
        <div style={{ display: 'flex', gap: '2rem' }}>
          <a href="/pricing" style={{ color: '#fff', textDecoration: 'none' }}>Pricing</a>
          <a href="/contact" style={{ color: '#fff', textDecoration: 'none' }}>Contact</a>
        </div>
      </nav>

      <section style={{ textAlign: 'center', marginBottom: '6rem' }}>
        <h1 style={{ fontSize: '3.5rem', marginBottom: '1rem', lineHeight: 1.2 }}>
          Levqor — The Self-Driven<br />Automation Engine
        </h1>
        <p style={{ fontSize: '1.25rem', color: '#aaa', marginBottom: '3rem', maxWidth: '600px', margin: '0 auto 3rem' }}>
          Automate your business with AI-powered workflows. No cron jobs, no plugins. Just intelligent automation that runs itself.
        </p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '4rem' }}>
          <a href="#demo" style={{
            backgroundColor: '#fff',
            color: '#000',
            padding: '1rem 2rem',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 600
          }}>
            Watch it Think
          </a>
          <a href="/pricing" style={{
            backgroundColor: 'transparent',
            color: '#fff',
            padding: '1rem 2rem',
            border: '2px solid #fff',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 600
          }}>
            Start Free
          </a>
        </div>

        <div id="demo" style={{
          width: '100%',
          maxWidth: '800px',
          margin: '0 auto',
          aspectRatio: '16/9',
          backgroundColor: '#111',
          borderRadius: '12px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          border: '1px solid #333'
        }}>
          <video
            controls
            style={{ width: '100%', height: '100%', borderRadius: '12px' }}
            poster="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 450'%3E%3Crect fill='%23111' width='800' height='450'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' fill='%23666' font-size='24' font-family='sans-serif'%3EDemo Video Placeholder%3C/text%3E%3C/svg%3E"
          >
            <source src="/demo.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      </section>

      <section style={{ marginBottom: '6rem' }}>
        <h2 style={{ fontSize: '2.5rem', textAlign: 'center', marginBottom: '3rem' }}>How It Works</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
          {[
            { title: 'Describe Your Workflow', desc: 'Tell Levqor what you need in plain English. No complex setup required.' },
            { title: 'AI Plans & Executes', desc: 'Our AI engine understands your intent and builds the automation pipeline automatically.' },
            { title: 'Monitor & Optimize', desc: 'Watch your workflows run, get insights, and let AI continuously improve performance.' }
          ].map((feature, i) => (
            <div key={i} style={{
              padding: '2rem',
              backgroundColor: '#111',
              borderRadius: '12px',
              border: '1px solid #333'
            }}>
              <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>{feature.title}</h3>
              <p style={{ color: '#aaa', lineHeight: 1.6 }}>{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ textAlign: 'center', marginBottom: '4rem' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '2rem' }}>Ready to Automate Everything?</h2>
        <a href="/pricing" style={{
          backgroundColor: '#fff',
          color: '#000',
          padding: '1rem 2.5rem',
          borderRadius: '8px',
          textDecoration: 'none',
          fontWeight: 600,
          display: 'inline-block'
        }}>
          Get Started Free
        </a>
      </section>

      <footer style={{
        borderTop: '1px solid #333',
        paddingTop: '2rem',
        marginTop: '4rem',
        textAlign: 'center',
        color: '#666',
        fontSize: '0.875rem'
      }}>
        <div style={{ marginBottom: '1rem' }}>
          <a href="/privacy" style={{ color: '#666', margin: '0 1rem' }}>Privacy</a>
          <a href="/terms" style={{ color: '#666', margin: '0 1rem' }}>Terms</a>
          <a href="/contact" style={{ color: '#666', margin: '0 1rem' }}>Contact</a>
        </div>
        <div>© 2025 Levqor. All rights reserved.</div>
      </footer>
    </main>
  )
}
