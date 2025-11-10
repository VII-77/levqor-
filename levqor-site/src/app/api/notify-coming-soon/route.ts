import { NextResponse } from 'next/server';
import { writeFileSync, readFileSync, existsSync } from 'fs';
import { join } from 'path';

const NOTIFY_FILE = '/tmp/notify_coming_soon.json';

interface NotifyEntry {
  email: string;
  connector: string;
  timestamp: string;
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { email, connector } = body;

    if (!email || !connector) {
      return NextResponse.json(
        { ok: false, error: 'email and connector required' },
        { status: 400 }
      );
    }

    const entry: NotifyEntry = {
      email,
      connector,
      timestamp: new Date().toISOString(),
    };

    let entries: NotifyEntry[] = [];
    if (existsSync(NOTIFY_FILE)) {
      const content = readFileSync(NOTIFY_FILE, 'utf-8');
      entries = JSON.parse(content);
    }

    entries.push(entry);
    writeFileSync(NOTIFY_FILE, JSON.stringify(entries, null, 2));

    if (process.env.RESEND_API_KEY) {
      try {
        await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
          },
          body: JSON.stringify({
            from: 'Levqor <notify@levqor.ai>',
            to: email,
            subject: `We'll notify you when ${connector} is ready`,
            html: `
              <h2>Thanks for your interest in ${connector}!</h2>
              <p>We'll send you an email as soon as ${connector} integration is available on Levqor.</p>
              <p>In the meantime, you can explore our other connectors and start automating your workflows.</p>
              <p>Best,<br>The Levqor Team</p>
            `,
          }),
        });
      } catch (emailError) {
        console.error('Failed to send confirmation email:', emailError);
      }
    }

    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error('Notify error:', error);
    return NextResponse.json(
      { ok: false, error: 'internal_error' },
      { status: 500 }
    );
  }
}
