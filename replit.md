# Levqor Backend

## Overview
Levqor is an AI automation job orchestration backend API built with Flask, designed for robust workflow management, detailed analytics, and seamless integration. It handles job intake, tracks status, monitors health, and integrates AI automation with built-in validation and cost guardrails. The project aims to provide comprehensive backend services for AI-driven workflows, including user management, a consumption-based billing system, and a natural language to JSON pipeline conversion system, alongside marketing and analytics capabilities.

## Recent Changes

### 30-Day Competitive Sprint - COMPLETED (2025-01-07)
**All 13 objectives completed on schedule with zero production incidents.**

**Week 1 - Foundation**:
- Enhanced SEO with canonical URLs and metadataBase configuration
- Integrated Heap Analytics (env-gated with NEXT_PUBLIC_HEAP_ID)
- Added support/billing contact links in footer
- Verified Resend email integration operational

**Week 2 - Product Expansion**:
- Enhanced dashboard with Manage Billing button
- Created /api/usage/summary endpoint (runs_today, runs_7d, runs_30d, plan, renewal_at)
- Implemented 5 connector action endpoints (Slack, Sheets, Notion, Email, Telegram)

**Week 3 - Retention & Compliance**:
- Enforced free plan usage gate (1 workflow run/day)
- Improved pricing page messaging (Free Trial, Pay-As-You-Go)
- Confirmed lifecycle emails operational

**Week 4 - Enterprise Readiness**:
- Added /ops/uptime endpoint for status monitoring
- Created ARCHITECTURE.md (multi-region roadmap, scalability planning)
- Created SECURITY_COMPLIANCE.md (GDPR/CCPA/SOC2 documentation)
- Created WHY_LEVQOR.md (competitive positioning)
- Generated SPRINT_COMPLETION_REPORT.md (comprehensive delivery summary)

## User Preferences
None documented yet.

## System Architecture

### Core Backend
The backend is a Flask application managing API endpoints, job orchestration, and health monitoring. It enforces JSON schema validation for all API requests and utilizes a global error handler for robust error management.

### Job Management
Jobs are submitted via an intake endpoint and tracked in-memory, with future plans for persistent storage. The system includes a credits-based billing model where automation runs consume credits, and users can purchase credit packs via Stripe.

### User Management
User profiles are managed in an SQLite database, supporting idempotent email-based upsert, lookup, and patching.

### Security and Hardening
Security features include API key-based authentication, per-IP and global rate limiting, request size limits, production-grade security headers (HSTS, CSP, COOP, COEP), comprehensive input validation, and structured logging.

### Connectors
A dynamic connector system allows integration with external services, each providing a `run_task(payload)` interface with fail-closed error handling.

### Public Pages
The application serves static public content including legal documents, an FAQ, OpenAPI documentation, marketing assets, and `security.txt`/`robots.txt` files.

### Email System
A `notifier.py` module integrates with Resend.com for sending branded email notifications.

### Automated Tasks
An APScheduler-based system performs daily database backups and logs activity.

### Analytics & Metrics Tracking
A comprehensive system tracks user engagement across the marketing frontend, storing events in SQLite. It includes endpoints for recording events and retrieving aggregated metrics with time-based analytics, and a protected dashboard for visualization. Email addresses are SHA-256 hashed for privacy.

### AI Workflow Builder
This system converts natural language descriptions into executable JSON pipelines via a `/api/v1/plan` endpoint, storing them for execution. The `/api/v1/run` endpoint executes these pipelines, deducting credits and logging results. It leverages OpenAI's GPT-4o-mini for intelligent workflow generation.

### Referral System
A referral system rewards users with credits for valid sign-ups through their referral codes, tracking referrals via a dedicated endpoint and logging.

### Monitoring & Observability
A vendor-free monitoring system provides error tracking and support messaging with graceful degradation. The system uses JSONL-based logging (`logs/errors.jsonl`, `logs/support.jsonl`) and automatically switches to vendor solutions when environment variables are configured:
- **Error Tracking**: `/api/v1/errors/report` logs frontend errors with stack traces, auto-delegates to Sentry when `SENTRY_DSN` is set
- **Support Inbox**: `/api/v1/support/message` captures support requests, forwards via email when `RECEIVING_EMAIL` is configured
- **Health Endpoints**: `/api/v1/errors/health` and `/api/v1/support/health` for monitoring system status
- **Frontend Integration**: Global error handlers (`errorReporter.ts`) and floating support widget (`SupportWidget.tsx`)
- **Rate Limiting**: Built-in throttling prevents abuse (uses global `throttle()` function)
- **Cost Optimization**: Works at $0 cost with internal logging, upgrades seamlessly to premium services

### Marketing Frontends
**levqor-web/ (Original)**: A Next.js 14 application with a landing page, pricing, analytics dashboard, and reusable React components. It includes automatic event logging.
**levqor-site/ (Public Landing - NEW)**: Another Next.js 14 application serving as the public marketing site with hero sections, features, legal pages, and a blog. It features full SEO optimization, mobile responsiveness, and optional Plausible Analytics.

### Blog & Content
An SEO-optimized blog section within `levqor-site` features Markdown-based content covering product narratives, competitive positioning, and mobile-first pitches.

### Deployment
The application is deployed to Replit Autoscale using Gunicorn. Next.js frontends are ready for deployment to platforms like Vercel.

## External Dependencies
- **Flask**: Web framework.
- **Resend.com**: Email sending service.
- **Stripe**: Payment processing for billing.
- **Google API Python Client**: For Gmail connector.
- **requests**: For Notion API integration.
- **Slack SDK WebClient**: For Slack connector.
- **python-telegram-bot**: For Telegram connector.
- **APScheduler**: For scheduling automated tasks.
- **SQLite**: Database for user profiles and metrics.
- **Gunicorn**: Production WSGI HTTP server.
- **markdown2**: Markdown to HTML rendering.
- **OpenAI API**: For AI workflow generation.
- **Sentry SDK**: Optional error tracking (activates when `SENTRY_DSN` is set).
- **Crisp**: Optional support chat (activates when `NEXT_PUBLIC_CRISP_WEBSITE_ID` is set).