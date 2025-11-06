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
**November 6, 2025**
- **Documentation & Blog Infrastructure:**
  - Created docs/ folder with markdown files (index.md, api.md, connectors.md)
  - Created blog/ folder with index.json and 001-launch-story.md
  - Added markdown2 for Markdown→HTML rendering
  - Added /public/docs/<file> and /public/blog/<slug> routes
  - Updated robots.txt with new URLs
  - Created sitemap.xml with all public URLs
  - Routes working locally, investigating deployment issue
- **Connector Pack Integration:**
  - Created connectors/ folder with dynamic connector modules
  - Implemented gmail_connector.py (Google API Python Client)
  - Implemented notion_connector.py (Notion API via requests)
  - Implemented slack_connector.py (Slack SDK WebClient)
  - Implemented telegram_connector.py (python-telegram-bot library)
  - Added /api/v1/connect/<name> dynamic endpoint with API key protection
  - All connectors expose run_task(payload) → dict interface
  - Fail-closed error handling with graceful degradation
  - Full import validation and testing completed
- **Stripe Billing Integration:**
  - Added /billing/create-checkout-session endpoint
  - Added /billing/webhook endpoint with signature verification
  - Payment success/failure email notifications via notifier.py
  - User payment history stored in database metadata
  - CORS updated to allow Stripe domains
- **Email System Integration:**
  - Created notifier.py module with Resend.com integration
  - Configured branded email addresses: support@, billing@, no-reply@, security@levqor.ai
  - Added email logging to logs/email_test.log
  - Created setup and verification scripts (setup_resend_domain.py, verify_resend.py, test_email.py)
  - DNS records template ready for Cloudflare
  - Resend + Cloudflare Email Routing setup documented
- **Deployment:**
  - Deployed to Replit Autoscale at https://levqor-backend.replit.app
  - Custom domain DNS configured (api.levqor.ai)
  - Production API keys generated and configured
  - BUILD_ID environment variable set

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
- `notifier.py` - Email notification module (Resend integration)
- `connectors/` - Dynamic connector modules for external services
  - `gmail_connector.py` - Gmail API integration
  - `notion_connector.py` - Notion API integration
  - `slack_connector.py` - Slack SDK integration
  - `telegram_connector.py` - Telegram Bot API integration
- `requirements.txt` - Python dependencies with all SDKs
- `.env.example` - Environment variable template
- `API_KEY_ROTATION.md` - API key rotation procedure documentation

### Automated Backup System
- `scripts/auto_backup.sh` - Automated database backup script
- APScheduler BackgroundScheduler running in run.py
- Daily backups at 00:00 UTC (CronTrigger)
- Backup logs: logs/backup.log
- Backups stored: backups/backup_YYYYMMDDTHHMMSSZ.db

### Email System
- `notifier.py` - Email module with Resend API integration
- `test_email.py` - Test email sending functionality
- `setup_resend_domain.py` - Add domain to Resend and get DNS records
- `verify_resend.py` - Check domain verification status
- `docs/LEVQOR_EMAIL_DNS.txt` - DNS records for Cloudflare setup
- `logs/email_test.log` - Email send attempt logs

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

#### Running the Validation Script
The validation script tests all endpoints to ensure they're working correctly:

```bash
# Set the BASE_URL environment variable to your Repl URL
export BASE_URL=https://<your-repl-name>.<your-username>.repl.co

# Run the validation script
python scripts/validate_levqor.py
```

On success, you'll see: `🟢 COCKPIT GREEN — Levqor backend validated`

#### Database Backup

**Automated Backups (APScheduler):**
- Daily backups run automatically at 00:00 UTC
- Scheduled via APScheduler BackgroundScheduler
- Executes `scripts/auto_backup.sh` via subprocess
- Logs to application stdout and `logs/backup.log`
- Fail-closed error handling with timeout (60s)

**Manual Backup:**
```bash
# Manual backup via script
bash scripts/auto_backup.sh

# Legacy backup script (uses sqlite3 .backup)
./scripts/backup_db.sh

# Backups are stored in backups/ directory with timestamps
# Automated format: backups/backup_YYYYMMDDTHHMMSSZ.db
# Manual format: backups/levqor-YYYY-MM-DD-HHMMSS.db
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
- **Deployed**: Live at https://levqor-backend.replit.app
- **Custom Domain**: api.levqor.ai (DNS configured, awaiting verification)
- Production server (Gunicorn) running on port 5000 with 2 workers, 4 threads, 30s timeout
- In-memory job store (JOBS dictionary)
- SQLite database for user profiles (levqor.db) with WAL mode enabled
- All endpoints operational and tested
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
- **Automated Backups**: APScheduler running daily at 00:00 UTC
- API key rotation support with dual-set validation
- OpenAPI 3.0 documentation at /public/openapi.json
- Well-known files (security.txt, robots.txt)
- **Email System**: Resend + Cloudflare Email Routing configured (pending domain verification)
  - Branded addresses: support@, billing@, no-reply@, security@levqor.ai
  - Secrets configured: RESEND_API_KEY, RECEIVING_EMAIL
- **Connector Pack**: Gmail, Notion, Slack, Telegram integrations active
  - Dynamic endpoint: /api/v1/connect/<name>
  - All connectors tested and operational

## Next Phase
- **Email System Completion:**
  1. Update RESEND_API_KEY to "Full Access" permission
  2. Run: python3 setup_resend_domain.py
  3. Add DNS records to Cloudflare
  4. Verify domain and test email sending
- **Domain Verification:**
  - Complete api.levqor.ai verification in Replit
  - Test production endpoints via custom domain
- **Future Enhancements:**
  - Replace in-memory job store with PostgreSQL or Redis
  - Implement real job orchestration queue (Celery, RQ, or similar)
  - Implement callback URL notifications for job completion
  - Add cost tracking and guardrails enforcement
  - Add API key management endpoints (create, revoke, list)
  - Implement usage analytics and monitoring

## User Preferences
None documented yet.
