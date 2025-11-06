# Levqor Backend

## Overview
Levqor is an AI automation job orchestration backend API built with Flask. It provides job intake, status tracking, health monitoring, and integrates AI automation with validation and cost guardrails. The project aims to offer robust workflow management, detailed analytics, and seamless integration with various external services.

## User Preferences
None documented yet.

## System Architecture

### Core Backend
The backend is a Flask application (`run.py`) handling API endpoints, job orchestration, and health monitoring. It uses JSON schema validation for all API requests and features a global error handler for robust error management.

### Job Management
Jobs are submitted via a `/api/v1/intake` endpoint and their status can be tracked. Currently, job storage is in-memory, with plans to integrate a persistent database.

### User Management
User profiles are managed using an SQLite database (`levqor.db`) with WAL mode enabled for concurrency. It supports idempotent email-based user upsert, lookup, and patching.

### Security and Hardening
- **Authentication**: API key-based authentication (`X-Api-Key` header) for all write operations, supporting zero-downtime key rotation.
- **Rate Limiting**: Per-IP and global rate limits to prevent abuse.
- **Request Limits**: Maximum request body and payload size limits are enforced.
- **Security Headers**: Production-grade headers like HSTS, CSP, COOP, COEP are implemented.
- **Input Validation**: Comprehensive JSON schema validation and field length constraints.
- **Logging**: Structured logging for requests and exceptions.

### Connectors
A dynamic connector system (`connectors/` folder) allows integration with external services. Each connector exposes a `run_task(payload)` interface with fail-closed error handling.

### Public Pages
The application serves static public content including legal documents (privacy, terms, cookies), an FAQ page, OpenAPI documentation, and well-known files (`security.txt`, `robots.txt`). Marketing assets and documentation are also served.

### Email System
A dedicated `notifier.py` module integrates with Resend.com for sending branded email notifications (support, billing, no-reply, security).

### Automated Tasks
An APScheduler-based system performs daily database backups, logging to `logs/backup.log`.

### Deployment
The application is deployed to Replit Autoscale, utilizing Gunicorn as the production server. Custom domain (api.levqor.ai) is configured.

## External Dependencies
- **Flask**: Web framework.
- **Resend.com**: Email sending service.
- **Stripe**: Payment processing for billing.
- **Google API Python Client**: For Gmail connector.
- **Notion API**: Accessed via `requests` library for Notion connector.
- **Slack SDK WebClient**: For Slack connector.
- **python-telegram-bot**: For Telegram connector.
- **APScheduler**: For scheduling automated tasks (e.g., database backups).
- **SQLite**: In-memory and disk-based database for user profiles.
- **Gunicorn**: Production WSGI HTTP server.
- **markdown2**: Markdown to HTML rendering.

## Recent Changes
**November 6, 2025**
- **Automated Backup System Enhancement:**
  - Added `misfire_grace_time=900` (±15 min tolerance) to APScheduler configuration
  - Implemented immediate backup validation on server startup
  - Verified daily backup schedule (00:00 UTC) working correctly
  - Backup format: `backups/backup_YYYYMMDDTHHMMSSZ.db`
  - All backup activity logged to `logs/backup.log`
  - Script location: `scripts/auto_backup.sh` (executable)

- **Marketing Assets & SEO:**
  - Created `marketing/landing_snippets.json` with headlines, CTAs, USPs
  - Added `marketing/testimonials.json` with customer reviews
  - Implemented `/api/v1/marketing/summary` endpoint for analytics
  - Added OpenGraph and Twitter Card meta tags to all docs/blog pages
  - Enhanced social sharing capabilities across documentation