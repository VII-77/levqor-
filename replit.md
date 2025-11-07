# Levqor Backend

## Overview
Levqor is a job orchestration backend API built with Flask, providing AI automation with validation and cost guardrails. The backend handles job intake, status tracking, and provides health monitoring endpoints.

## Purpose
- Job orchestration and workflow management
- JSON schema validation for job requests
- In-memory job storage (ready for database integration)
- Health monitoring and metrics reporting
- Legal documentation and FAQ pages

## Recent Changes
**November 7, 2025**
- Deployed frontend to Vercel (https://levqor.ai)
- Frontend and backend fully connected and operational
- **Frontend Authentication Built from Scratch:**
  - Created Next.js 14 app with TypeScript
  - Integrated NextAuth v5 with Resend magic link authentication
  - Added protected dashboard with session management
  - Created sign-in flow with email verification
  - Using existing RESEND_API_KEY secret (manual integration, not Replit connector)
  - Frontend source code now available in `levqor-site/` directory
  - Deployment script: `deploy_frontend_complete.sh`
  - SessionProvider wrapper for client-side auth
  - Complete documentation in `AUTH_SETUP_COMPLETE.md`
- **Operational Monitoring Added:**
  - Created `public_smoke.sh` automated testing script (10/10 tests passing)
  - Added operational health endpoints (Phase-4 enhanced versions deployed)
  - Added JWT_SECRET for future authentication support
  - Fixed LSP errors in run.py (None type validation)
  - All triage requirements met
- **Secrets Configured:**
  - JWT_SECRET (auth token signing)
  - STRIPE_SECRET_KEY (payment processing)
  - STRIPE_WEBHOOK_SECRET (webhook verification)
  - RESEND_API_KEY (email delivery, used for NextAuth magic links)
  - DATABASE_URL (PostgreSQL connection)
- **Integration Notes:**
  - Resend connector (connector:ccfg_resend_01K69QKYK789WN202XSE3QS17V) available but not used
  - Using manual RESEND_API_KEY secret instead for more control
  - Future: Consider using Replit integrations for OAuth providers

**November 5, 2025**
- Initial setup of Levqor backend
- Created Flask application with all core endpoints
- Configured CORS and security headers for levqor.ai
- Added legal documentation (privacy policy, terms of service, cookie notice)
- Added FAQ page
- Created validation script for endpoint testing
- Configured workflow to run on port 5000
- Fixed deployment health checks with root (/) endpoint
- Switched to Gunicorn production server with 2 workers, 4 threads, 30s timeout
- Added user profile management with SQLite database
- Implemented idempotent email-based user upsert
- Added user lookup, get, and patch endpoints
- **Security Layer Added:**
  - API key authentication for all POST/PATCH routes (X-Api-Key header)
  - Rate limiting: 20 requests/minute per IP, 200 requests/minute global
  - Structured logging with IP and User-Agent tracking
  - Global error handler with exception logging
  - Protected /api/v1/ops/health endpoint
- **Database Optimizations:**
  - SQLite WAL mode enabled for better concurrency
  - Email index for fast user lookups
  - PRAGMA optimizations (journal_mode=WAL, synchronous=NORMAL)
  - Database backup script with WAL-aware copying
- Fixed database path to use SQLITE_PATH (avoiding PostgreSQL DATABASE_URL conflict)
- **Production-Grade Hardening:**
  - Complete security headers: HSTS, CSP, COOP, COEP
  - Request size limits: 512KB max body, 200KB max payload
  - Rate-limit response headers with Retry-After
  - URL and field validation with FormatChecker
  - Manual HTTP(S) protocol validation for callback URLs
  - Gunicorn environment variable tuning
  - Version and build info in root endpoint
  - Well-known files (security.txt, robots.txt)
  - API key rotation support with API_KEYS_NEXT
  - OpenAPI documentation endpoint
  - All production tests passing

## Project Architecture

### Backend Structure
- `run.py` - Main Flask application with API endpoints
- `requirements.txt` - Python dependencies (Flask 3.0.0, jsonschema 4.22.0, requests 2.32.5, gunicorn 23.0.0)
- `.env.example` - Environment variable template
- `API_KEY_ROTATION.md` - API key rotation procedure documentation

### Frontend Structure
- `levqor-site/` - Next.js 14 application with TypeScript
  - `src/app/` - App Router pages and layouts
  - `src/app/page.tsx` - Landing page
  - `src/app/signin/page.tsx` - Sign-in page with email form
  - `src/app/signin/verify/page.tsx` - Email verification confirmation page
  - `src/app/dashboard/page.tsx` - Protected dashboard (requires authentication)
  - `src/auth.ts` - NextAuth v5 configuration with Resend provider
  - `src/middleware.ts` - Route protection middleware
  - `package.json` - Next.js dependencies (next 14.2.15, next-auth 5.0.0-beta.22, resend 4.0.1)
  - `.env.local` - Local development environment variables
  - `.gitignore` - Git ignore configuration
- `deploy_frontend_complete.sh` - Complete Vercel deployment script with build and env setup
- `setup_auth.sh` - Authentication setup script (fixed for NextAuth v5 compatibility)
- `AUTH_SETUP_COMPLETE.md` - Complete authentication setup documentation

### Public Pages
- `public/legal/privacy.html` - Privacy policy
- `public/legal/terms.html` - Terms of service
- `public/legal/cookies.html` - Cookie notice
- `public/faq/index.html` - FAQ page
- `public/.well-known/security.txt` - Security contact information
- `public/robots.txt` - Search engine crawling directives
- `public/openapi.json` - OpenAPI 3.0 API documentation

### Scripts
- `scripts/validate_levqor.py` - Endpoint validation script
- `scripts/backup_db.sh` - Database backup script with WAL support
- `public_smoke.sh` - Automated smoke testing for all public endpoints
- `triage_and_fix.sh` - Live triage and fix script (from user)
- `deploy_frontend.sh` - Deploy frontend to Vercel with environment variables

#### Running the Validation Script
The validation script tests all endpoints to ensure they're working correctly:

```bash
# Set the BASE_URL environment variable to your Repl URL
export BASE_URL=https://<your-repl-name>.<your-username>.repl.co

# Run the validation script
python scripts/validate_levqor.py
```

On success, you'll see: `🟢 COCKPIT GREEN — Levqor backend validated`

#### Public Smoke Tests
Automated testing of all public endpoints:

```bash
# Test backend endpoints
BACKEND=https://api.levqor.ai ./public_smoke.sh
```

Tests:
- Core endpoints (/, /health, /status)
- Operations endpoints (/ops/uptime, /ops/queue_health, /billing/health)
- Public content (/public/metrics, /public/openapi.json)
- API v1 endpoints (job creation, status checking)

On success: `✅ All smoke tests passed! 🎉`

#### Database Backup
Create consistent backups of the SQLite database:

```bash
# Backup the database
./scripts/backup_db.sh

# Backups are stored in backups/ directory with timestamps
# Format: backups/levqor-YYYY-MM-DD-HHMMSS.db
# Note: Script uses sqlite3 .backup if available, otherwise copies DB + WAL/SHM files
```

### API Endpoints

#### Root & Health
- `GET /` - Root endpoint for deployment health checks
  - Returns: `{"ok": true, "service": "levqor-backend", "version": "1.0.0"}`

- `GET /health` - Health check endpoint
  - Returns: `{"ok": true, "ts": <timestamp>}`
  
- `GET /public/metrics` - Public metrics
  - Returns: `{"uptime_rolling_7d": 99.99, "jobs_today": 0, "audit_coverage": 100, "last_updated": <timestamp>}`

#### Job Management
- `POST /api/v1/intake` - Submit a new job (requires API key)
  - Headers: `X-Api-Key: <your-api-key>`
  - Body: `{"workflow": "string", "payload": {}, "callback_url": "string", "priority": "low|normal|high"}`
  - Returns: `{"job_id": "uuid", "status": "queued"}` (202 Accepted)
  
- `GET /api/v1/status/<job_id>` - Check job status (public)
  - Returns: `{"job_id": "uuid", "status": "queued|running|succeeded|failed", "created_at": <timestamp>, "result": {}, "error": {}}`

#### Development
- `POST /api/v1/_dev/complete/<job_id>` - Simulate job completion (dev only, requires API key)
  - Headers: `X-Api-Key: <your-api-key>`
  - Body: `{"result": {}}`
  - Returns: `{"ok": true}`

#### Operations
- `GET /api/v1/ops/health` - Protected health check endpoint (requires API key)
  - Headers: `X-Api-Key: <your-api-key>`
  - Returns: `{"ok": true, "ts": <timestamp>}`

- `GET /ops/uptime` - Public system uptime and health (Phase-4 enhanced)
  - Returns: `{"status": "operational", "services": {"api": "operational", "database": "operational"}, "version": "1.0.0", ...}`

- `GET /ops/queue_health` - Public job queue health monitoring (Phase-4 enhanced)
  - Returns: `{"depth": 0, "dlq": 0, "mode": "sync", "queue_available": false, "retry": 0}`

- `GET /billing/health` - Public Stripe integration health (Phase-4 enhanced)
  - Returns: `{"status": "operational", "stripe": true, "available": [...], "pending": [...]}`

#### User Management
- `POST /api/v1/users/upsert` - Create or update user by email (idempotent, requires API key)
  - Headers: `X-Api-Key: <your-api-key>`
  - Body: `{"email": "user@example.com", "name": "Name", "locale": "en-GB", "currency": "GBP|USD|EUR", "meta": {}}`
  - Returns: `{"created": true, "user": {...}}` (201) or `{"updated": true, "user": {...}}` (200)
  
- `GET /api/v1/users?email=<email>` - Lookup user by email (public)
  - Returns: User object (200) or `{"error": "not_found"}` (404)
  
- `GET /api/v1/users/<user_id>` - Get user by ID (public)
  - Returns: User object (200) or `{"error": "not_found"}` (404)
  
- `PATCH /api/v1/users/<user_id>` - Update user fields (requires API key)
  - Headers: `X-Api-Key: <your-api-key>`
  - Body: `{"name": "New Name", "locale": "en-US", "currency": "USD", "meta": {"key": "value"}}`
  - Returns: `{"updated": true, "user": {...}}` (200)

### Security & CORS
- **Authentication:**
  - API key-based authentication for all POST/PATCH routes
  - Keys passed via `X-Api-Key` header
  - Development mode: When `API_KEYS` env var not set, all requests allowed
  - Production: Set `API_KEYS` environment variable (comma-separated values)
  - Zero-downtime key rotation via `API_KEYS_NEXT` (see API_KEY_ROTATION.md)
- **Rate Limiting:**
  - Per-IP burst limit: 20 requests/minute (configurable via `RATE_BURST`)
  - Global limit: 200 requests/minute (configurable via `RATE_GLOBAL`)
  - Returns 429 (Too Many Requests) when limits exceeded
  - Response headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After
- **Request Limits:**
  - Maximum request body: 512KB (configurable via `MAX_CONTENT_LENGTH`)
  - Maximum job payload: 200KB
  - Workflow name: 1-128 characters
  - Callback URL: 1-1024 characters, must be valid HTTP(S)
- **Logging:**
  - Structured logging for all requests (method, path, IP, User-Agent)
  - Exception logging with full traceback
  - Log level: INFO
- **CORS:**
  - Configured for `https://levqor.ai`
  - Allowed methods: GET, POST, OPTIONS, PATCH
  - Allowed headers: Content-Type, Authorization, X-Api-Key
- **Security Headers (Production-Grade):**
  - Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  - Content-Security-Policy: default-src 'none'; connect-src https://levqor.ai https://api.levqor.ai; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'
  - Cross-Origin-Opener-Policy: same-origin
  - Cross-Origin-Embedder-Policy: require-corp
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - Referrer-Policy: strict-origin-when-cross-origin
  - Permissions-Policy: geolocation=(), microphone=()
- **Input Validation:**
  - JSON schema validation with FormatChecker for all API requests
  - Field length constraints on all inputs
  - Manual HTTP(S) protocol validation for callback URLs
  - Global error handler to prevent information leakage

### Current State
- **Production Deployed**: Both frontend and backend live
  - Backend: https://api.levqor.ai (Replit Autoscale)
  - Frontend: https://levqor.ai (Vercel - ready for redeployment with auth)
  - Frontend source code available in `levqor-site/` directory
- Production server (Gunicorn) running on port 5000 with 2 workers, 4 threads, 30s timeout
- PostgreSQL database (Neon) for production data
- SQLite database for local development (levqor.db) with WAL mode enabled
- **All systems operational:**
  - 10/10 smoke tests passing
  - Health checks: ✅ PASSING
  - Queue monitoring: ✅ ACTIVE
  - Stripe integration: ✅ OPERATIONAL
  - Database: ✅ CONNECTED
- Deployment configured for Autoscale with environment variable tuning
- Root endpoint (/) with version and build info
- User management with email-based idempotent upsert
- Production-grade security: HSTS, CSP, COOP, COEP headers
- Comprehensive security layer with API key auth and rate limiting
- Rate-limit response headers (X-RateLimit-*, Retry-After)
- Request size limits (512KB body, 200KB payload)
- URL and field validation with length constraints
- Structured logging for all requests
- Database backup script for consistent snapshots
- API key rotation support with dual-set validation
- OpenAPI 3.0 documentation at /public/openapi.json
- Well-known files (security.txt, robots.txt)
- Automated smoke testing with public_smoke.sh
- JWT_SECRET configured for future authentication

## Next Phase
- Replace in-memory job store with PostgreSQL or Redis
- Implement real job orchestration queue (Celery, RQ, or similar)
- Implement callback URL notifications for job completion
- Add cost tracking and guardrails enforcement
- Add API key management endpoints (create, revoke, list)
- Implement usage analytics and monitoring
- Deploy to production environment with API_KEYS configured

## User Preferences
None documented yet.
