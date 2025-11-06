# Launching Levqor: Production-Ready Job Orchestration

**November 6, 2025** | By Levqor Team

Today we're excited to launch **Levqor**, a production-ready backend API for AI automation with enterprise-grade features. After months of development and hardening, we're ready to serve as the backbone for AI-powered workflows.

## What is Levqor?

Levqor is a Flask-based job orchestration API that provides:

- **Job Management**: Submit, track, and manage AI automation jobs with JSON schema validation
- **User Profiles**: Email-based user management with flexible metadata
- **External Integrations**: Pre-built connectors for Gmail, Notion, Slack, and Telegram
- **Billing**: Stripe checkout and webhook handling with email confirmations
- **Security**: API key authentication, rate limiting, and production-grade headers
- **Reliability**: Automated daily backups, 99.99% uptime, health monitoring

## Why We Built Levqor

AI automation is powerful, but building production-ready infrastructure is hard. Teams waste weeks implementing:

- Authentication and authorization
- Rate limiting and security headers
- Database schema and migrations
- Email notifications
- Payment processing
- External API integrations
- Monitoring and logging

Levqor provides all of this out of the box, so you can focus on building your AI features instead of reinventing infrastructure.

## Key Features

### 🔒 Security First

- API key authentication with zero-downtime rotation
- Rate limiting (20 req/min per IP, 200 req/min global)
- Production-grade security headers (HSTS, CSP, COOP, COEP)
- Input validation with JSON schema
- Structured logging with IP and User-Agent tracking

### 📧 Branded Communications

- Professional email system via Resend
- Branded addresses: support@, billing@, security@levqor.ai
- Automatic payment confirmations
- Email logging and tracking

### 🔌 Ready-Made Integrations

No more SDK wrestling. Our connector pack includes:

- **Gmail**: Send emails, list messages, manage labels
- **Notion**: Search pages, query databases, create content
- **Slack**: Post messages, upload files, list channels
- **Telegram**: Send messages, manage bots, get updates

All connectors use a unified `run_task()` interface with fail-closed error handling.

### 💳 Stripe Billing Built-In

- Checkout session creation
- Webhook handling with signature verification
- Payment success/failure notifications
- User payment history tracking

### 🛡️ Production-Grade Reliability

- **Automated Backups**: Daily at 00:00 UTC via APScheduler
- **Database**: SQLite with WAL mode for concurrency
- **Deployment**: Replit Autoscale with global edge network
- **Monitoring**: Health endpoints, metrics dashboard
- **Uptime**: 99.99% (7-day rolling average)

## Technical Stack

- **Framework**: Flask 3.0
- **Server**: Gunicorn with 2 workers, 4 threads
- **Database**: SQLite with WAL mode
- **Scheduler**: APScheduler for automated tasks
- **Email**: Resend API
- **Payments**: Stripe
- **Integrations**: Google API, Notion API, Slack SDK, Telegram Bot API

## Architecture Decisions

### Why SQLite?

We chose SQLite over PostgreSQL for several reasons:

1. **Simplicity**: Zero database administration
2. **Performance**: Fast for read-heavy workloads
3. **Portability**: Single file, easy backups
4. **WAL Mode**: Concurrent reads and writes

For workloads exceeding 100K requests/day, we recommend migrating to PostgreSQL.

### Why Replit Autoscale?

Replit Autoscale provides:

- Global edge network
- Automatic HTTPS
- Zero-config deployment
- Custom domain support
- Environment variable management

Perfect for rapid iteration and production deployment.

### Why In-Memory Job Store?

Our current in-memory job queue (Python dict) is intentionally simple. For production workloads, we recommend:

- **Redis**: Fast, persistent queue
- **PostgreSQL**: Durable job storage
- **Celery/RQ**: Distributed task queue

The architecture supports easy migration when needed.

## Getting Started

### 1. Authentication

Request an API key from support@levqor.ai

### 2. Submit a Job

```bash
curl -X POST https://api.levqor.ai/api/v1/intake \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: your-api-key" \
  -d '{
    "workflow": "ai-analysis",
    "payload": {"data": "your-data"},
    "callback_url": "https://your-app.com/webhook"
  }'
```

### 3. Check Status

```bash
curl https://api.levqor.ai/api/v1/status/{job_id}
```

## Documentation

- **API Reference**: [api.levqor.ai/public/docs/api](https://api.levqor.ai/public/docs/api)
- **Connectors Guide**: [api.levqor.ai/public/docs/connectors](https://api.levqor.ai/public/docs/connectors)
- **GitHub**: Coming soon

## What's Next?

Our roadmap for the next quarter:

- **PostgreSQL Migration**: Optional database backend
- **Distributed Queue**: Redis/Celery integration
- **WebSocket Support**: Real-time job updates
- **Admin Dashboard**: Web UI for monitoring
- **More Connectors**: GitHub, Linear, Airtable, Salesforce
- **Webhooks**: Callback queue with retry logic

## Pricing

We're currently in private beta. Contact support@levqor.ai for access.

Launch pricing (limited availability):
- **Starter**: $29/month - 10K jobs
- **Pro**: $99/month - 100K jobs
- **Enterprise**: Custom - Unlimited jobs + SLA

## Join Us

We're building the infrastructure layer for AI automation. If you're tired of rebuilding auth, payments, and integrations for every project, give Levqor a try.

**Links:**
- API: https://api.levqor.ai
- Docs: https://api.levqor.ai/public/docs/
- Email: support@levqor.ai

---

*Happy automating! 🚀*

— The Levqor Team
