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
**November 5, 2025**
- Initial setup of Levqor backend
- Created Flask application with all core endpoints
- Configured CORS and security headers for levqor.ai
- Added legal documentation (privacy policy, terms of service, cookie notice)
- Added FAQ page
- Created validation script for endpoint testing
- Configured workflow to run on port 5000
- Fixed deployment health checks with root (/) endpoint
- Switched to Gunicorn production server
- Added user profile management with SQLite database
- Implemented idempotent email-based user upsert
- Added user lookup, get, and patch endpoints

## Project Architecture

### Backend Structure
- `run.py` - Main Flask application with API endpoints
- `requirements.txt` - Python dependencies (Flask 3.0.0, jsonschema 4.22.0, requests 2.32.5, gunicorn 23.0.0)
- `.env.example` - Environment variable template

### Public Pages
- `public/legal/privacy.html` - Privacy policy
- `public/legal/terms.html` - Terms of service
- `public/legal/cookies.html` - Cookie notice
- `public/faq/index.html` - FAQ page

### Scripts
- `scripts/validate_levqor.py` - Endpoint validation script

#### Running the Validation Script
The validation script tests all endpoints to ensure they're working correctly:

```bash
# Set the BASE_URL environment variable to your Repl URL
export BASE_URL=https://<your-repl-name>.<your-username>.repl.co

# Run the validation script
python scripts/validate_levqor.py
```

On success, you'll see: `🟢 COCKPIT GREEN — Levqor backend validated`

### API Endpoints

#### Root & Health
- `GET /` - Root endpoint for deployment health checks
  - Returns: `{"ok": true, "service": "levqor-backend", "version": "1.0.0"}`

- `GET /health` - Health check endpoint
  - Returns: `{"ok": true, "ts": <timestamp>}`
  
- `GET /public/metrics` - Public metrics
  - Returns: `{"uptime_rolling_7d": 99.99, "jobs_today": 0, "audit_coverage": 100, "last_updated": <timestamp>}`

#### Job Management
- `POST /api/v1/intake` - Submit a new job
  - Body: `{"workflow": "string", "payload": {}, "callback_url": "string", "priority": "low|normal|high"}`
  - Returns: `{"job_id": "uuid", "status": "queued"}` (202 Accepted)
  
- `GET /api/v1/status/<job_id>` - Check job status
  - Returns: `{"job_id": "uuid", "status": "queued|running|succeeded|failed", "created_at": <timestamp>, "result": {}, "error": {}}`

#### Development
- `POST /api/v1/_dev/complete/<job_id>` - Simulate job completion (dev only)
  - Body: `{"result": {}}`
  - Returns: `{"ok": true}`

#### User Management
- `POST /api/v1/users/upsert` - Create or update user by email (idempotent)
  - Body: `{"email": "user@example.com", "name": "Name", "locale": "en-GB", "currency": "GBP|USD|EUR", "meta": {}}`
  - Returns: `{"created": true, "user": {...}}` (201) or `{"updated": true, "user": {...}}` (200)
  
- `GET /api/v1/users?email=<email>` - Lookup user by email
  - Returns: User object (200) or `{"error": "not_found"}` (404)
  
- `GET /api/v1/users/<user_id>` - Get user by ID
  - Returns: User object (200) or `{"error": "not_found"}` (404)
  
- `PATCH /api/v1/users/<user_id>` - Update user fields
  - Body: `{"name": "New Name", "locale": "en-US", "currency": "USD", "meta": {"key": "value"}}`
  - Returns: `{"updated": true, "user": {...}}` (200)

### Security & CORS
- CORS configured for `https://levqor.ai`
- Security headers: X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy
- JSON schema validation for all API requests

### Current State
- Production server (Gunicorn) running on port 5000
- In-memory job store (JOBS dictionary)
- SQLite database for user profiles (levqor.db)
- All endpoints operational and tested
- Deployment configured for Autoscale
- Root endpoint (/) available for health checks
- User management with email-based idempotent upsert
- Ready for production database migration (PostgreSQL or Redis)

## Next Phase
- Replace in-memory job store with PostgreSQL or Redis
- Implement real job orchestration queue (Celery, RQ, or similar)
- Add authentication and API key management
- Implement callback URL notifications
- Add cost tracking and guardrails enforcement
- Deploy to production environment

## User Preferences
None documented yet.
