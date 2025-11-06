# Levqor Documentation

Welcome to the Levqor backend documentation. Levqor is a production-ready job orchestration API built with Flask, providing AI automation with validation and cost guardrails.

## Overview

Levqor provides a secure, scalable backend for managing AI-powered workflows with enterprise-grade features:

- **Job Orchestration**: Submit, track, and manage AI automation jobs
- **User Management**: Email-based user profiles with flexible metadata
- **External Integrations**: Gmail, Notion, Slack, and Telegram connectors
- **Billing Integration**: Stripe checkout and webhook handling
- **Email Notifications**: Branded email system via Resend
- **Automated Backups**: Daily database snapshots

## Quick Start

### Authentication

All POST and PATCH endpoints require API key authentication:

```bash
curl -X POST https://api.levqor.ai/api/v1/intake \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: your-api-key" \
  -d '{"workflow": "example", "payload": {}}'
```

### Submit a Job

```bash
POST /api/v1/intake
{
  "workflow": "ai-analysis",
  "payload": {"data": "your-data"},
  "callback_url": "https://your-app.com/webhook",
  "priority": "normal"
}
```

### Check Job Status

```bash
GET /api/v1/status/{job_id}
```

## Documentation Sections

- [API Reference](api) - Complete endpoint documentation
- [Connectors Guide](connectors) - Using external integrations

## Support

- Email: support@levqor.ai
- Documentation: https://api.levqor.ai/public/docs/
- Status: 99.99% uptime (7-day rolling)

## Production Endpoints

- **API**: https://api.levqor.ai
- **Deployment**: Replit Autoscale
- **Region**: Global edge network
