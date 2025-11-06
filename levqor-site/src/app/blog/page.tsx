import fs from 'fs'
import path from 'path'

export const metadata = {
  title: 'Blog — Levqor',
  description: 'Automation insights, product updates, and best practices from the Levqor team.',
}

interface Post {
  slug: string
  title: string
  date: string
  excerpt: string
}

function getPosts(): Post[] {
  const contentDir = path.join(process.cwd(), 'content')
  
  if (!fs.existsSync(contentDir)) {
    return []
  }
  
  const files = fs.readdirSync(contentDir).filter(f => f.endsWith('.md'))
  
  return files.map(file => {
    const content = fs.readFileSync(path.join(contentDir, file), 'utf-8')
    const frontmatterMatch = content.match(/^---\n([\s\S]+?)\n---/)
    const frontmatter = frontmatterMatch ? frontmatterMatch[1] : ''
    
    const titleMatch = frontmatter.match(/title: (.+)/)
    const dateMatch = frontmatter.match(/date: (.+)/)
    const excerptMatch = frontmatter.match(/excerpt: (.+)/)
    
    return {
      slug: file.replace('.md', ''),
      title: titleMatch ? titleMatch[1] : file,
      date: dateMatch ? dateMatch[1] : '',
      excerpt: excerptMatch ? excerptMatch[1] : ''
    }
  }).sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
}

export default function Blog() {
  const posts = getPosts()
  
  return (
    <main style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <nav style={{ marginBottom: '4rem' }}>
        <a href="/" style={{ color: '#fff', textDecoration: 'none', fontSize: '1.5rem', fontWeight: 'bold' }}>← Levqor</a>
      </nav>

      <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Blog</h1>
      <p style={{ color: '#aaa', marginBottom: '3rem' }}>Automation insights, product updates, and best practices.</p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        {posts.map(post => (
          <article key={post.slug} style={{
            backgroundColor: '#111',
            padding: '2rem',
            borderRadius: '12px',
            border: '1px solid #333'
          }}>
            <h2 style={{ fontSize: '1.75rem', marginBottom: '0.5rem' }}>
              <a href={`/blog/${post.slug}`} style={{ color: '#fff', textDecoration: 'none' }}>
                {post.title}
              </a>
            </h2>
            <p style={{ color: '#666', fontSize: '0.875rem', marginBottom: '1rem' }}>{post.date}</p>
            <p style={{ color: '#aaa', lineHeight: 1.6 }}>{post.excerpt}</p>
            <a href={`/blog/${post.slug}`} style={{ color: '#fff', marginTop: '1rem', display: 'inline-block' }}>
              Read more →
            </a>
          </article>
        ))}
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
          <a href="/contact" style={{ color: '#666', margin: '0 1rem' }}>Contact</a>
        </div>
      </footer>
    </main>
  )
}
