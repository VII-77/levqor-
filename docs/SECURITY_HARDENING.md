# Security Hardening Guide

## Overview
This document describes the security controls implemented in Levqor Phase-4 Hardening.

## Security Headers

### Implementation
All security headers are controlled by the `SECURITY_HEADERS_ENABLED` flag.

### Headers Applied

#### Content-Security-Policy (CSP)
```
default-src 'self';
img-src * blob: data:;
script-src 'self' 'unsafe-inline' 'unsafe-eval' https://plausible.io;
style-src 'self' 'unsafe-inline';
connect-src 'self' https:
```

**Purpose**: Prevent XSS attacks by restricting resource loading

**Trade-offs**:
- `unsafe-inline` for scripts: Required for some frontend frameworks
- `unsafe-eval`: Required for dynamic code execution (consider removing)
- `https://plausible.io`: Allow analytics

#### Strict-Transport-Security (HSTS)
```
max-age=15552000; includeSubDomains
```

**Purpose**: Force HTTPS connections for 180 days

**Note**: Only enable in production with valid HTTPS certificate

#### X-Frame-Options
```
DENY
```

**Purpose**: Prevent clickjacking attacks

#### X-Content-Type-Options
```
nosniff
```

**Purpose**: Prevent MIME type sniffing

#### Referrer-Policy
```
strict-origin-when-cross-origin
```

**Purpose**: Control referrer information in requests

#### Permissions-Policy
```
camera=(), microphone=(), geolocation=()
```

**Purpose**: Disable unused browser features

## Rate Limiting

### Configuration

#### Free Plan
- **Per API Key**: 60 requests/minute
- **Per IP**: 30 requests/minute

#### Pro Plan
- **Per API Key**: 600 requests/minute
- **Per IP**: 120 requests/minute

### Implementation
- Token bucket algorithm
- Redis-backed (distributed)
- Memory fallback (single-process)

### Response Format
```json
{
  "error": "rate_limited",
  "message": "API key rate limit exceeded",
  "retry_after": 45,
  "limit": 60,
  "scope": "api_key"
}
```

### Bypass
Rate limiting can be temporarily disabled:
```bash
export RATELIMIT_ENABLED=false
```

## Webhook Signature Verification

### Supported Providers

#### Stripe
- **Header**: `Stripe-Signature`
- **Algorithm**: HMAC SHA-256
- **Secret**: `STRIPE_WEBHOOK_SECRET`

#### Slack
- **Headers**: `X-Slack-Request-Timestamp`, `X-Slack-Signature`
- **Algorithm**: HMAC SHA-256
- **Freshness**: 5 minutes
- **Secret**: `SLACK_SIGNING_SECRET`

#### Telegram
- **Validation**: `update_id` presence
- **Secret**: Bot token in URL path

#### Generic (Notion, GitHub)
- **Header**: `X-Hub-Signature-256` or `X-Notion-Signature`
- **Algorithm**: Configurable HMAC
- **Secret**: Provider-specific env var

### Usage
```python
from webhooks.verify import webhook_auth_required

@app.route("/webhooks/stripe", methods=["POST"])
@webhook_auth_required("stripe")
def stripe_webhook():
    # Signature already verified
    payload = request.get_json()
    # Process webhook
```

### Enforcement
Controlled by `WEBHOOK_VERIFY_ALL` flag:
- `true`: Reject all webhooks without valid signatures
- `false`: Log warnings but allow through

## Abuse Controls

### Device Binding (Free Plan)

**Purpose**: Prevent account sharing on free tier

**Mechanism**:
1. First request creates device fingerprint hash
2. Track ASN (network) changes
3. Allow max 3 device/network changes per 24 hours
4. Block further changes with upgrade prompt

**Fingerprint**:
- User-Agent
- Accept-Language
- SHA-256 hashed (privacy)

### Referral Anti-Fraud

**Purpose**: Prevent referral abuse

**Rules**:
1. Max 5 signups/day from same ASN
2. Email hashes stored (privacy)
3. Log blocks for analysis

**Bypass**:
```bash
export ABUSE_GUARDS_ENABLED=false
```

## Encryption & Secrets

### Secrets Storage
- **Environment Variables**: All secrets
- **Never Logged**: Automatic redaction in logs
- **Rotation**: Manual via env var updates

### Secrets Required
```bash
# Core
DATABASE_URL          # PostgreSQL connection
SESSION_SECRET        # Flask session signing

# Optional (Graceful Degradation)
REDIS_URL            # Queue system
SENTRY_DSN           # Error tracking

# Payments
STRIPE_SECRET_KEY    # Stripe API
STRIPE_WEBHOOK_SECRET # Webhook verification

# Email
RESEND_API_KEY       # Email sending

# Connectors
SLACK_WEBHOOK_URL
TELEGRAM_BOT_TOKEN
NOTION_API_KEY
GOOGLE_SERVICE_ACCOUNT_JSON
```

### Secret Rotation Procedure

**Step 1: Generate New Secret**
```bash
# Example: Stripe webhook secret
# 1. Go to Stripe Dashboard → Webhooks
# 2. Reveal secret for your endpoint
# 3. Copy new secret
```

**Step 2: Update Environment**
```bash
# In Replit: Secrets tab
STRIPE_WEBHOOK_SECRET=whsec_NEW_SECRET
```

**Step 3: Test**
```bash
curl -X POST https://your-domain.com/webhooks/stripe/test
```

**Step 4: Restart**
```bash
# Restart application to load new secret
```

## Database Security

### Connection Security
- SSL/TLS enforced
- Password-based authentication
- Connection pooling

### Backup Security
- Daily automated backups
- 7-day retention
- Encrypted at rest (provider-managed)
- Restore drill verification

### Query Safety
- Parameterized queries only
- No dynamic SQL construction
- Input validation on all endpoints

## API Security

### Authentication
- API key in header: `X-API-Key`
- Per-key rate limiting
- Key rotation supported

### Authorization
- User-scoped resources
- Admin endpoints protected
- Webhook endpoints verified

### Input Validation
- JSON schema validation
- Type checking
- Size limits (5MB max)

## Monitoring & Alerting

### Sentry Integration
```bash
export SENTRY_DSN=https://...@sentry.io/...
```

**Captures**:
- Unhandled exceptions
- Error-level logs
- 10% transaction sampling
- 10% profiling sampling

### Metrics Exposed
```
/metrics endpoint (Prometheus format)

- api_latency_p95_ms
- queue_depth
- dlq_depth
- error_rate_total
- connector_5xx_total
- rate_limit_hits_total
- ai_cost_daily_usd
- device_blocks_total
- referral_blocks_total
```

### Log Security
- Sensitive data redacted automatically
- 24-hour rotation
- JSON format for parsing
- Access controlled

## Compliance

### GDPR
- Email hashing for privacy
- Device fingerprint hashing
- Data retention policies
- Right to deletion support

### PCI DSS
- No card data stored
- Stripe handles PCI compliance
- Webhook verification enforced

### SOC 2
- Audit logging
- Access controls
- Incident response procedures
- Backup & recovery tested

## Incident Response

### Security Incident Procedure

**Step 1: Detect & Assess**
- Check Sentry for unusual patterns
- Review `/metrics` for anomalies
- Check `logs/errors.jsonl`

**Step 2: Contain**
```bash
# Disable affected feature
export FEATURE_ENABLED=false

# Block malicious IPs (if applicable)
# Add to rate limiter

# Rotate compromised secrets
```

**Step 3: Investigate**
- Review access logs
- Check database for unauthorized changes
- Analyze attack vectors

**Step 4: Remediate**
- Apply fixes
- Deploy patches
- Update security controls

**Step 5: Post-Mortem**
- Document timeline
- Identify root cause
- Implement prevention measures
- Notify affected users (if required)

## Security Checklist

### Pre-Deployment
- [ ] All secrets configured
- [ ] HTTPS enabled
- [ ] Security headers active
- [ ] Rate limiting tested
- [ ] Webhook verification enabled
- [ ] Backup system verified

### Monthly Review
- [ ] Review Sentry errors
- [ ] Check rate limit patterns
- [ ] Audit abuse control blocks
- [ ] Update dependencies
- [ ] Rotate API keys
- [ ] Test restore process

### Quarterly Audit
- [ ] Penetration testing
- [ ] Dependency vulnerability scan
- [ ] Access control review
- [ ] Compliance check
- [ ] Incident response drill

## Known Limitations

1. **CSP `unsafe-inline`**: Required for some frameworks, increases XSS risk
2. **Memory-based rate limiting**: Not distributed, resets on restart
3. **Device fingerprinting**: Can be bypassed with privacy tools
4. **ASN-based fraud detection**: Coarse granularity, may have false positives

## Recommended Enhancements

### Short-term (1-3 months)
1. Implement WAF (Cloudflare/AWS WAF)
2. Add bot detection (reCAPTCHA)
3. Enhance CSP (remove `unsafe-inline`)
4. Add 2FA for user accounts

### Long-term (6-12 months)
1. Security audit by third party
2. SOC 2 Type II certification
3. Advanced fraud detection (ML-based)
4. Zero-trust architecture

---

*Last Updated: 2025-11-07*
*Version: 4.0*
*Classification: Internal*
