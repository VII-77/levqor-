# Levqor System Architecture

## Overview
Levqor is a production-ready AI job orchestration platform designed to compete with Zapier and Make.com. The system follows a modern microservices-inspired architecture with enterprise-grade reliability patterns.

## System Components

### 1. Backend API (Flask)
**Location**: `run.py`
**Responsibilities**:
- RESTful API endpoints for workflow orchestration
- User authentication via Supabase JWT
- Stripe billing integration with webhook handling
- Rate limiting and security middleware
- Health monitoring and observability
- Automated task scheduling (daily backups)

**Key Technologies**:
- Flask + Gunicorn (WSGI server)
- SQLite for user profiles and metrics
- APScheduler for cron jobs
- Resend.com for transactional emails

### 2. Frontend Dashboard (Next.js 14)
**Location**: `levqor/frontend/`
**Responsibilities**:
- User dashboard with usage analytics
- Subscription management
- Workflow builder interface
- Referral system UI
- Error reporting and support widget

**Key Technologies**:
- Next.js 14 (App Router)
- TypeScript
- Supabase authentication client
- Heap/Plausible analytics

### 3. Connector System
**Location**: `connectors/`
**Design Pattern**: Dynamic plugin architecture
**Supported Integrations**:
- Slack (webhook messages)
- Google Sheets (row append)
- Notion (page creation)
- Gmail (via Resend fallback)
- Telegram (bot messages)

Each connector implements a `run_task(payload)` interface with fail-closed error handling.

### 4. Data Layer

#### SQLite Database
**Tables**:
- `users`: User profiles, credits, referral codes
- `usage_daily`: Daily usage metrics (jobs_run, cost_saving)
- `referrals`: Referral tracking with UTM parameters
- `events`: Marketing analytics events (hashed PII)

#### File-Based Storage
- `data/pipelines/`: JSON workflow definitions
- `data/jobs.jsonl`: Execution logs
- `logs/errors.jsonl`: Frontend error tracking
- `logs/support.jsonl`: Support messages

### 5. AI Workflow Builder
**Endpoint**: `/api/v1/plan`
**Technology**: OpenAI GPT-4o-mini
**Process**:
1. Accept natural language description
2. Convert to structured JSON pipeline
3. Store in `data/pipelines/`
4. Return pipeline ID for execution

**Endpoint**: `/api/v1/run`
**Process**:
1. Load pipeline from storage
2. Check free plan gates (1 run/day)
3. Deduct credits
4. Execute actions sequentially
5. Log results

## Multi-Region Architecture (Future)

### Current State (Single Region)
- Deployed to Replit Autoscale (single US region)
- No geographic redundancy
- Database is local SQLite

### Phase 1: Database Migration
**Target**: Q1 2025
1. Migrate from SQLite to PostgreSQL (Neon)
2. Enable point-in-time recovery
3. Implement connection pooling
4. Add read replicas

### Phase 2: Multi-Region Deployment
**Target**: Q2 2025
1. Deploy API to multiple regions (US-East, US-West, EU-West)
2. Implement geo-routing via Cloudflare
3. Database replication across regions
4. Global load balancing

### Phase 3: Edge Computing
**Target**: Q3 2025
1. Move static assets to CDN
2. Deploy read-only endpoints to edge
3. Implement cache layers (Redis)
4. Regional failover automation

## Security Architecture

### Authentication & Authorization
- Supabase JWT-based auth
- API key-based service authentication
- Scoped permissions (future)

### Data Protection
- SHA-256 hashing for email addresses in analytics
- Secrets managed via environment variables
- No PII in logs or error tracking
- HTTPS-only (enforced via HSTS)

### Rate Limiting
- Global: 100 req/min
- Per-IP: 20 req/min
- Billing endpoints: throttled
- Free plan: 1 workflow run/day

### Security Headers
- HSTS: Strict-Transport-Security
- CSP: Content-Security-Policy
- COOP: Cross-Origin-Opener-Policy
- COEP: Cross-Origin-Embedder-Policy

## Monitoring & Observability

### Health Endpoints
- `/health`: Basic liveness check
- `/ops/uptime`: Detailed uptime monitoring for status pages
- `/api/v1/ops/health`: Comprehensive health check
- `/api/v1/errors/health`: Error tracking status
- `/api/v1/support/health`: Support inbox status

### Error Tracking
- Internal JSONL logging (free)
- Auto-delegates to Sentry when `SENTRY_DSN` set
- Frontend global error handlers
- Stack trace capture

### Support System
- Internal JSONL inbox (free)
- Auto-forwards via email when `RECEIVING_EMAIL` set
- Floating support widget in UI
- Auto-delegates to Crisp when `NEXT_PUBLIC_CRISP_WEBSITE_ID` set

### Metrics & Analytics
- User engagement tracking
- Daily usage aggregation
- Conversion funnel analysis
- Dashboard: `/api/v1/analytics/dashboard`

## Deployment Architecture

### Current Production
**Platform**: Replit Autoscale
**Config**: `run.py` + Gunicorn
**Workers**: 2 (configurable via `GUNICORN_WORKERS`)
**Threads**: 4 per worker
**Timeout**: 30s request timeout
**Graceful Shutdown**: 20s

### CI/CD (Roadmap)
**Phase 1** (Current):
- Manual deployment via Replit
- No automated testing pipeline
- Direct production updates

**Phase 2** (Planned):
- GitHub Actions for testing
- Automated deploy previews
- Staging environment
- Blue-green deployments

## Scalability Considerations

### Current Bottlenecks
1. **Database**: SQLite limited to ~100 req/s
2. **Storage**: File-based pipelines don't scale
3. **Connectors**: Synchronous execution only

### Scaling Plan
1. **Short-term** (0-1K users):
   - Current architecture sufficient
   - Monitor usage patterns
   - Optimize slow queries

2. **Mid-term** (1K-10K users):
   - Migrate to PostgreSQL
   - Add job queue (Redis + Celery)
   - Async connector execution
   - Implement caching layer

3. **Long-term** (10K+ users):
   - Kubernetes deployment
   - Horizontal auto-scaling
   - Distributed job processing
   - Multi-region database replication

## Cost Model

### Infrastructure Costs (Current)
- Backend hosting: $0 (Replit free tier)
- Database: $0 (SQLite local)
- Email: $0.001/email (Resend)
- AI workflows: $0.01/run (OpenAI API)

### Target Economics
- CAC: $15 per user
- LTV: $180 (12 months * $15 ARPU)
- Gross margin: 80%
- Break-even: 1,000 paying users

## Disaster Recovery

### Backup Strategy
**Daily Automated Backups**:
- Schedule: 00:00 UTC
- Script: `scripts/auto_backup.sh`
- Retention: 7 days
- Storage: Local filesystem (future: S3)

### Recovery Procedures
1. **Database corruption**: Restore from daily backup
2. **API outage**: Restart Gunicorn workers
3. **Data loss**: Point-in-time recovery (future with PostgreSQL)

### RTO/RPO Targets
- **Recovery Time Objective (RTO)**: 4 hours
- **Recovery Point Objective (RPO)**: 24 hours

## Future Enhancements

### Q1 2025
- [ ] Migrate to PostgreSQL
- [ ] Add async job queue
- [ ] Implement webhook retry logic
- [ ] Team/multi-user support

### Q2 2025
- [ ] Multi-region deployment
- [ ] Advanced analytics dashboard
- [ ] Workflow versioning
- [ ] API rate limit tiers

### Q3 2025
- [ ] Marketplace for connectors
- [ ] Custom connector SDK
- [ ] Enterprise SSO
- [ ] Compliance certifications (SOC 2)

## Contact
For architecture questions: tech@levqor.ai
