export async function GET(req: Request, { params }: { params: { path: string[] } }) {
  const url = new URL(req.url);
  url.host = 'api.levqor.ai';
  url.protocol = 'https:';
  url.pathname = '/' + params.path.join('/');
  
  const r = await fetch(url.toString(), {
    headers: {
      'Authorization': req.headers.get('authorization') ?? ''
    }
  });
  
  return new Response(await r.text(), {
    status: r.status,
    headers: {
      'content-type': r.headers.get('content-type') ?? 'application/json'
    }
  });
}

export async function POST(req: Request, ctx: any) {
  return GET(req, ctx);
}
