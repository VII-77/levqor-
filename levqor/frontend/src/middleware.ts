import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const supabaseToken = request.cookies.get('sb-access-token')?.value
  const { pathname } = request.nextUrl

  if (pathname.startsWith('/dashboard')) {
    if (!supabaseToken) {
      return NextResponse.redirect(new URL('/signup', request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*']
}
