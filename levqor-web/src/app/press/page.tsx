import { Metadata } from 'next';
import fs from 'fs';
import path from 'path';

export const metadata: Metadata = {
  title: 'Press Kit - Levqor',
  description: 'Levqor press kit with brand assets, product information, and media resources.',
  alternates: {
    canonical: 'https://app.levqor.ai/press',
  },
  openGraph: {
    title: 'Press Kit - Levqor',
    description: 'Brand assets, product information, and media resources for Levqor.',
    type: 'website',
    url: 'https://app.levqor.ai/press',
    images: [
      {
        url: '/og/launch.jpg',
        width: 1200,
        height: 630,
        alt: 'Levqor Press Kit',
      },
    ],
  },
};

function getPressKitContent() {
  try {
    const filePath = path.join(process.cwd(), '..', 'marketing', 'press_kit.md');
    return fs.readFileSync(filePath, 'utf-8');
  } catch {
    return '# Press Kit\n\nContent not available.';
  }
}

function renderMarkdown(markdown: string) {
  const lines = markdown.split('\n');
  const htmlLines: string[] = [];
  let inList = false;
  let inCodeBlock = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (line.startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      if (inCodeBlock) {
        htmlLines.push('<pre style="background: #f5f5f5; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 16px 0;">');
      } else {
        htmlLines.push('</pre>');
      }
      continue;
    }

    if (inCodeBlock) {
      htmlLines.push(line.replace(/</g, '&lt;').replace(/>/g, '&gt;'));
      continue;
    }

    if (line.startsWith('# ')) {
      htmlLines.push(`<h1 style="font-size: 2.5rem; font-weight: 700; margin: 32px 0 16px; color: #0066cc;">${line.slice(2)}</h1>`);
    } else if (line.startsWith('## ')) {
      htmlLines.push(`<h2 style="font-size: 2rem; font-weight: 700; margin: 28px 0 14px; color: #333;">${line.slice(3)}</h2>`);
    } else if (line.startsWith('### ')) {
      htmlLines.push(`<h3 style="font-size: 1.5rem; font-weight: 600; margin: 24px 0 12px; color: #333;">${line.slice(4)}</h3>`);
    } else if (line.startsWith('---')) {
      htmlLines.push('<hr style="border: none; border-top: 2px solid #e0e0e0; margin: 32px 0;">');
    } else if (line.startsWith('- ') || line.startsWith('* ')) {
      if (!inList) {
        htmlLines.push('<ul style="margin: 12px 0; padding-left: 24px;">');
        inList = true;
      }
      htmlLines.push(`<li style="margin: 8px 0;">${line.slice(2)}</li>`);
    } else if (line.startsWith('**') && line.endsWith('**')) {
      const text = line.slice(2, -2);
      const parts = text.split(':');
      if (parts.length === 2) {
        htmlLines.push(`<p style="margin: 12px 0;"><strong style="color: #0066cc;">${parts[0]}:</strong> ${parts[1]}</p>`);
      } else {
        htmlLines.push(`<p style="margin: 12px 0;"><strong>${text}</strong></p>`);
      }
    } else if (line.trim() === '') {
      if (inList) {
        htmlLines.push('</ul>');
        inList = false;
      }
      htmlLines.push('<br>');
    } else if (line.startsWith('>')) {
      htmlLines.push(`<blockquote style="border-left: 4px solid #0066cc; padding-left: 16px; margin: 16px 0; color: #666; font-style: italic;">${line.slice(2)}</blockquote>`);
    } else {
      let processed = line;
      processed = processed.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
      processed = processed.replace(/\*(.+?)\*/g, '<em>$1</em>');
      processed = processed.replace(/`(.+?)`/g, '<code style="background: #f0f0f0; padding: 2px 6px; border-radius: 4px; font-family: monospace;">$1</code>');
      processed = processed.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" style="color: #0066cc; text-decoration: none;" target="_blank" rel="noopener">$1</a>');
      htmlLines.push(`<p style="margin: 12px 0; line-height: 1.6;">${processed}</p>`);
    }
  }

  if (inList) {
    htmlLines.push('</ul>');
  }

  return htmlLines.join('\n');
}

export default function PressPage() {
  const pressKitMarkdown = getPressKitContent();
  const htmlContent = renderMarkdown(pressKitMarkdown);

  return (
    <div style={{
      maxWidth: '900px',
      margin: '0 auto',
      padding: '40px 20px',
      fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      color: '#333',
    }}>
      <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      
      <div style={{
        marginTop: '64px',
        padding: '32px',
        background: '#f9f9f9',
        borderRadius: '12px',
        textAlign: 'center',
      }}>
        <h3 style={{ fontSize: '1.5rem', marginBottom: '16px', color: '#0066cc' }}>
          For Press Inquiries
        </h3>
        <p style={{ fontSize: '1.1rem', color: '#666', marginBottom: '24px' }}>
          Contact us for interviews, product demos, or additional information
        </p>
        <a
          href="mailto:press@levqor.ai"
          style={{
            display: 'inline-block',
            padding: '14px 32px',
            background: '#0066cc',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '8px',
            fontWeight: 600,
            fontSize: '1.1rem',
          }}
        >
          Contact Press Team
        </a>
      </div>

      <div style={{
        marginTop: '32px',
        textAlign: 'center',
        fontSize: '0.9rem',
        color: '#999',
      }}>
        <p>Download Assets: <a href="/og/launch.jpg" download style={{ color: '#0066cc' }}>Launch Image</a> | <a href="/og/pricing.jpg" download style={{ color: '#0066cc' }}>Pricing Image</a></p>
        <p style={{ marginTop: '8px' }}>Last Updated: November 6, 2025</p>
      </div>
    </div>
  );
}
