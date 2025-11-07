/**
 * Frontend Security Headers Middleware
 * For Next.js applications - add to middleware.ts
 * 
 * Implements:
 * - Content Security Policy (CSP)
 * - Strict Transport Security (HSTS)
 * - X-Content-Type-Options
 * - X-Frame-Options
 * - Referrer-Policy
 */

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

/**
 * Content Security Policy configuration
 * Adjust directives based on your application needs
 */
const CSP_DIRECTIVES = {
  'default-src': ["'self'"],
  'script-src': [
    "'self'",
    "'unsafe-inline'",  // Remove in production, use hashes instead
    "'unsafe-eval'",    // Remove in production if possible
    'https://cdn.jsdelivr.net',
    'https://unpkg.com'
  ],
  'style-src': [
    "'self'",
    "'unsafe-inline'",  // Required for styled-components/emotion
    'https://fonts.googleapis.com'
  ],
  'img-src': [
    "'self'",
    'data:',
    'https:',
    'blob:'
  ],
  'font-src': [
    "'self'",
    'data:',
    'https://fonts.gstatic.com'
  ],
  'connect-src': [
    "'self'",
    'https://api.stripe.com',
    'https://*.vercel.app',
    process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
  ],
  'frame-ancestors': ["'none'"],
  'base-uri': ["'self'"],
  'form-action': ["'self'"]
}

function buildCSP(): string {
  return Object.entries(CSP_DIRECTIVES)
    .map(([key, values]) => `${key} ${values.join(' ')}`)
    .join('; ')
}

export function middleware(request: NextRequest) {
  const response = NextResponse.next()
  
  // Content Security Policy
  response.headers.set(
    'Content-Security-Policy',
    buildCSP()
  )
  
  // Strict Transport Security (HSTS)
  // Tells browsers to always use HTTPS for the next 2 years
  response.headers.set(
    'Strict-Transport-Security',
    'max-age=63072000; includeSubDomains; preload'
  )
  
  // Prevent MIME type sniffing
  response.headers.set(
    'X-Content-Type-Options',
    'nosniff'
  )
  
  // Prevent clickjacking attacks
  response.headers.set(
    'X-Frame-Options',
    'DENY'
  )
  
  // Control referrer information
  response.headers.set(
    'Referrer-Policy',
    'strict-origin-when-cross-origin'
  )
  
  // Permissions Policy (formerly Feature-Policy)
  response.headers.set(
    'Permissions-Policy',
    'camera=(), microphone=(), geolocation=()'
  )
  
  // Cross-Origin policies
  response.headers.set(
    'Cross-Origin-Opener-Policy',
    'same-origin'
  )
  
  response.headers.set(
    'Cross-Origin-Embedder-Policy',
    'require-corp'
  )
  
  response.headers.set(
    'Cross-Origin-Resource-Policy',
    'same-origin'
  )
  
  return response
}

// Configure which paths to apply middleware
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}

/**
 * USAGE INSTRUCTIONS:
 * 
 * 1. Save this file as: levqor-web/middleware.ts (or levqor-site/middleware.ts)
 * 
 * 2. For production CSP, replace 'unsafe-inline' with hash-based approach:
 *    - Run: npm run build
 *    - Check browser console for CSP violations
 *    - Add script hashes to script-src directive
 * 
 * 3. Test CSP compliance:
 *    - Open browser dev tools
 *    - Check Console for CSP violations
 *    - Adjust directives as needed
 * 
 * 4. Environment-specific configuration:
 *    - Development: More permissive CSP
 *    - Production: Strict CSP with hashes
 * 
 * Example hash-based script-src:
 *   'script-src': [
 *     "'self'",
 *     "'sha256-ABC123...'",  // Hash of inline script
 *   ]
 */
