# Levqor Backend

## Overview
Levqor is an enterprise-ready AI automation job orchestration backend API built with Flask. It provides production-grade workflow management with comprehensive security hardening (v6.0), asynchronous queue processing, real-time monitoring, a partner/affiliate system with automated payouts, revenue tracking, detailed analytics, and robust abuse controls. The platform focuses on operational safety, audit-hardened processes, SLO-based reliability, cost protection, GDPR compliance, and marketing automation capabilities, aiming to be a scalable growth engine for AI-driven automation.

**Latest Version**: v6.0 (Complete Production Maturity)
**Status**: Investor-Grade Platform ✅

## User Preferences
- **Resend Email:** Manual API key management preferred
- **Stripe:** Manual secret management in use
- **OpenAI:** Manual API key in use

## System Architecture

### Core Backend
The backend is a Flask application managing API endpoints, job orchestration, and health monitoring. It enforces JSON schema validation, utilizes a global error handler, and includes a credits-based billing model integrated with Stripe.

### Job Management
Jobs are submitted via an intake endpoint, processed asynchronously using RQ with DLQ and retry logic, and tracked in-memory with future plans for persistent storage.

### User Management
User profiles are managed in an SQLite database, supporting idempotent email-based upsert, lookup, and patching.

### Security and Hardening
Features include JWT token rotation with refresh tokens (15min/7day expiry), token revocation database, per-user rate limiting (60/min), API key-based authentication, production-grade security headers (HSTS, CSP, COOP, COEP with Next.js middleware), comprehensive input validation, webhook signature verification (Stripe, Slack, Telegram, generic HMAC), AES-128 PII encryption, and abuse controls with device binding and referral anti-fraud. Feature flags allow for controlled rollout of security enhancements.

### Connectors
A dynamic connector system allows integration with external services (e.g., Slack, Notion, Telegram, Email, Google Sheets), each providing a `run_task(payload)` interface with fail-closed error handling.

### Public Pages & Content
The application serves static public content including legal documents, FAQs, OpenAPI documentation, marketing assets, `security.txt`, and `robots.txt`. A separate Next.js 14 application (`levqor-site`) serves as the public marketing site with SEO optimization, mobile responsiveness, and a Markdown-based blog.

### Email System
A `notifier.py` module integrates with Resend.com for sending branded email notifications, including a 4-email onboarding sequence and automated billing emails.

### Automated Tasks
An APScheduler-based system performs daily database backups with SHA-256 checksum verification and optional Google Drive upload, logs activity, and includes automated backup restore validation, emergency rollback automation, SLO watchdog with auto-rollback on latency threshold breach, spend guard automation with daily limit protection, and partner payout processing via Stripe Connect.

### Analytics & Metrics Tracking
A comprehensive system tracks user engagement across the marketing frontend, storing events in SQLite. It includes endpoints for recording events and retrieving aggregated metrics with time-based analytics, a protected dashboard for visualization, and SHA-256 hashing of email addresses for privacy. Enhanced Prometheus metrics provide P95 latency, queue depth, error rates, connector 5xx, and AI costs.

### AI Workflow Builder
This system converts natural language descriptions into executable JSON pipelines via a `/api/v1/plan` endpoint, storing them for execution. The `/api/v1/run` endpoint executes these pipelines, deducting credits and logging results, leveraging OpenAI's GPT-4o-mini.

### Referral and Partner System
A referral system rewards users with credits for valid sign-ups. A comprehensive partner/affiliate system includes partner registration, 20% commission tracking on referred revenue via Stripe webhooks, automated Stripe Connect payouts ($50 minimum threshold), a partner dashboard with conversion funnel metrics, and an admin revenue dashboard for MRR/ARR tracking and commission processing.

### Monitoring & Observability
A vendor-free monitoring system provides error tracking and support messaging with graceful degradation. It uses JSONL-based logging and automatically integrates with Sentry when `SENTRY_DSN` is set, and forwards support requests via email when `RECEIVING_EMAIL` is configured. Health endpoints (`/ops/queue_health`, `/ops/dlq/retry`, `/ops/uptime`) are available for system status monitoring. Telegram alerts are integrated for critical thresholds with 4 severity levels (critical, warning, info, success). Statistical anomaly detection monitors latency and error spikes using 3-sigma threshold. Cost dashboard aggregates metrics from Stripe, OpenAI, and infrastructure for unified cost tracking. SLO watchdog monitors 200ms P95 latency threshold with automatic rollback capability.

### Marketing Frontends
- **levqor-web/ (Original)**: Next.js 14 application with landing page, pricing, analytics dashboard, and reusable React components.
- **levqor-site/ (Public Landing - NEW)**: Next.js 14 marketing site with hero sections, features, legal pages, blog, SEO, and mobile responsiveness. Includes security headers middleware (CSP, HSTS, COOP), testimonials component with trust badges, and automated sitemap submission to search engines.

### Deployment
The Flask application is deployed to Replit Autoscale using Gunicorn. Next.js frontends are ready for deployment to platforms like Vercel.

## External Dependencies
- **Flask**: Web framework.
- **Resend.com**: Email sending service.
- **Stripe**: Payment processing for billing and webhooks.
- **Google API Python Client**: For Gmail connector.
- **requests**: For Notion API integration.
- **Slack SDK WebClient**: For Slack connector.
- **python-telegram-bot**: For Telegram connector.
- **APScheduler**: For scheduling automated tasks.
- **SQLite**: Database for user profiles and analytics events.
- **Gunicorn**: Production WSGI HTTP server.
- **markdown2**: Markdown to HTML rendering.
- **OpenAI API**: For AI workflow generation.
- **Sentry SDK**: Optional error tracking.
- **Crisp**: Optional support chat.
- **Buffer**: Social media integration for marketing automation.
- **Prometheus**: For metrics collection and monitoring.
- **Redis**: For async job queue (RQ) and rate limiting.
- **PostgreSQL**: Planned/migrated primary database.
- **PyJWT**: JWT token encoding/decoding for authentication.