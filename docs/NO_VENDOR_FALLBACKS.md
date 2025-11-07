# Vendor-Free Monitoring Fallbacks

## Overview

Levqor includes built-in error tracking and support chat that work **immediately at $0 cost**. When you later add Sentry or Crisp, the system automatically switches to those vendors seamlessly.

## Features

### 1. Error Tracking (Internal)
- **Endpoint:** `POST /api/v1/errors/report`
- **Storage:** `logs/errors.jsonl`
- **Alerts:** Email via Resend for errors/fatal
- **Rate Limit:** 60 errors per minute per IP
- **Auto-Switch:** Disabled when `SENTRY_DSN` is set

### 2. Support Inbox (Internal)
- **Endpoint:** `POST /api/v1/support/message`
- **Storage:** `logs/support.jsonl`
- **Forwarding:** Email to `RECEIVING_EMAIL` via Resend
- **Rate Limit:** 10 messages per minute per IP
- **Auto-Switch:** Disabled when `NEXT_PUBLIC_CRISP_WEBSITE_ID` is set

---

## API Endpoints

### Error Reporting

**POST /api/v1/errors/report**

```json
{
  "level": "error" | "fatal" | "warning",
  "message": "Error description",
  "stack": "Stack trace",
  "url": "https://app.levqor.ai/dashboard",
  "userAgent": "Mozilla/5.0...",
  "ts": 1699000000000,
  "release": "levqor@1.0.0",
  "user": {
    "id": "user_123",
    "email": "user@example.com"
  },
  "extra": {
    "custom": "data"
  }
}
```

**Response:** `{"status": "logged"}` or `{"status": "delegated_to_sentry"}`

**GET /api/v1/errors/health**

```json
{
  "collector": "internal" | "sentry",
  "status": "ok",
  "count_today": 42
}
```

### Support Messages

**POST /api/v1/support/message**

```json
{
  "email": "user@example.com",
  "subject": "Feature request",
  "message": "I would love to see...",
  "url": "https://app.levqor.ai/settings"
}
```

**Response:** `{"status": "sent"}` or `{"status": "use_crisp_widget"}`

**GET /api/v1/support/health**

```json
{
  "inbox": "internal" | "crisp",
  "status": "ok"
}
```

---

## Environment Variables

### Feature Flags (Default: enabled)

```bash
# Error Reporter
NEXT_PUBLIC_ENABLE_ERROR_REPORTER=true

# Support Widget
NEXT_PUBLIC_ENABLE_SUPPORT_WIDGET=true
```

### Vendor Integration (Auto-switch)

```bash
# When set, internal error tracking disabled automatically
SENTRY_DSN=https://abc123@o456.ingest.sentry.io/789

# When set, internal support widget disabled automatically
NEXT_PUBLIC_CRISP_WEBSITE_ID=abc12345-1234-1234-1234-123456789abc
```

### Configuration

```bash
# Email for support messages and error alerts
RECEIVING_EMAIL=support@levqor.ai

# API endpoint (optional, defaults to localhost:5000 in dev)
NEXT_PUBLIC_API_URL=https://api.levqor.ai

# App name for error tracking
NEXT_PUBLIC_APP_NAME=levqor
```

---

## Frontend Integration

### Error Reporter

**Auto-initialized** in `src/lib/errorReporter.ts`

**Global Handlers:**
- `window.onerror` - Catches runtime errors
- `window.onunhandledrejection` - Catches promise rejections

**Manual Capture:**

```typescript
import { errorReporter } from '@/lib/errorReporter';

// Capture exception
try {
  riskyOperation();
} catch (error) {
  errorReporter.captureException(error, { context: 'payment' });
}

// Capture message
errorReporter.captureMessage('Something unusual happened', 'warning');
```

**Throttling:** Max 5 errors per minute per session

### Support Widget

**Component:** `src/components/SupportWidget.tsx`

**Usage:**

```tsx
import SupportWidget from '@/components/SupportWidget';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SupportWidget />
      </body>
    </html>
  );
}
```

**Features:**
- Floating button (bottom-right)
- Form: email, subject, message
- Auto-prefills current URL
- Success/error toasts
- Mobile responsive

---

## Switchover Behavior

### Internal → Sentry

1. **Before:**
   - Frontend sends errors to `/api/v1/errors/report`
   - Backend logs to `logs/errors.jsonl`
   - Email alerts via Resend

2. **Add Sentry:**
   ```bash
   # Add to Replit Secrets
   SENTRY_DSN=https://...
   ```

3. **After:**
   - Frontend uses Sentry SDK (install `@sentry/nextjs`)
   - Backend endpoint returns `{"status": "delegated_to_sentry"}`
   - Internal logging disabled
   - Sentry dashboard shows all errors

### Internal → Crisp

1. **Before:**
   - Frontend shows support widget
   - Messages sent to `/api/v1/support/message`
   - Backend forwards via Resend

2. **Add Crisp:**
   ```bash
   # Add to Replit Secrets
   NEXT_PUBLIC_CRISP_WEBSITE_ID=abc12345-...
   ```

3. **After:**
   - Crisp chat widget loads automatically
   - Internal widget hidden
   - Backend endpoint returns `{"status": "use_crisp_widget"}`
   - Crisp dashboard shows all messages

---

## JSONL Log Format

### errors.jsonl

```json
{"ts":1699000000000,"level":"error","message":"Failed to load","stack":"Error: Failed...\n  at","url":"https://app.levqor.ai/","userAgent":"Mozilla/5.0...","release":"levqor","user_id":"user_123","ip":"192.168.1.1","extra":"{}"}
```

**Fields:**
- `ts` - Timestamp (milliseconds)
- `level` - error | fatal | warning
- `message` - Error message (max 500 chars)
- `stack` - Stack trace (max 2000 chars)
- `url` - Page URL (max 500 chars)
- `userAgent` - Browser info (max 200 chars)
- `release` - App version
- `user_id` - User ID (if authenticated)
- `ip` - Client IP
- `extra` - JSON extra data

**Rotation:** Manual (delete old logs periodically)

### support.jsonl

```json
{"ts":1699000000000,"email":"user@example.com","subject":"Feature request","message":"I would love...","url":"https://app.levqor.ai/settings","ip":"192.168.1.1"}
```

**Fields:**
- `ts` - Timestamp (milliseconds)
- `email` - User email
- `subject` - Message subject
- `message` - Full message (max 5000 chars)
- `url` - Page URL
- `ip` - Client IP

---

## Testing

### Test Error Reporting

```bash
# Manual test via curl
curl -X POST http://localhost:5000/api/v1/errors/report \
  -H "Content-Type: application/json" \
  -d '{
    "level": "error",
    "message": "Test error from curl",
    "stack": "test stack",
    "url": "/",
    "userAgent": "curl/test",
    "ts": '$(date +%s000)'
  }'

# Expected: {"status": "logged"}
# Check: logs/errors.jsonl should have new entry
# Check: Email alert sent to RECEIVING_EMAIL
```

### Test Support Message

```bash
curl -X POST http://localhost:5000/api/v1/support/message \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "subject": "Test support message",
    "message": "This is a test message from curl",
    "url": "/"
  }'

# Expected: {"status": "sent"}
# Check: logs/support.jsonl should have new entry
# Check: Email forwarded to RECEIVING_EMAIL
```

### Health Checks

```bash
# Error tracking health
curl http://localhost:5000/api/v1/errors/health
# Expected: {"collector":"internal","status":"ok","count_today":1}

# Support inbox health
curl http://localhost:5000/api/v1/support/health
# Expected: {"inbox":"internal","status":"ok"}
```

---

## Security

### Rate Limiting
- **Error reporting:** 60/min per IP
- **Support messages:** 10/min per IP
- **Body size:** 16KB max

### Data Privacy
- Emails redacted from error logs
- Support emails stored only in support.jsonl
- IP addresses logged for rate limiting
- Stack traces truncated (2000 chars)

### Fail-Closed Behavior
- Email send failures logged but don't crash API
- Invalid JSON silently skipped in health checks
- Rate limit errors return HTTP 429

---

## Cost Comparison

| Feature | Internal | Vendor |
|---------|----------|--------|
| **Error Tracking** | $0 | Sentry: $0-26/mo |
| **Support Chat** | $0 | Crisp: $0-25/mo |
| **Storage** | Disk (JSONL) | Cloud (unlimited) |
| **Retention** | Manual | 30-90 days |
| **Alerting** | Email (Resend) | Slack, PagerDuty, etc |
| **Dashboard** | None (JSONL logs) | Web UI, analytics |
| **Mobile App** | No | Yes (Crisp) |

**Recommendation:**
- **0-1K users:** Use internal (free)
- **1K-10K users:** Add Sentry ($26/mo)
- **10K+ users:** Add Crisp ($25/mo) + Sentry

---

## Monitoring Logs

### View Recent Errors

```bash
# Last 10 errors
tail -10 logs/errors.jsonl

# Errors from today
grep "$(date +%Y-%m-%d)" logs/errors.jsonl

# Fatal errors only
grep '"level":"fatal"' logs/errors.jsonl

# Pretty print (requires jq)
cat logs/errors.jsonl | jq -c
```

### View Support Messages

```bash
# Last 10 messages
tail -10 logs/support.jsonl

# Messages from specific email
grep '"email":"user@example.com"' logs/support.jsonl

# Count total messages
wc -l logs/support.jsonl
```

---

## Troubleshooting

### Errors not being logged

1. Check rate limit (60/min per IP)
2. Verify `NEXT_PUBLIC_ENABLE_ERROR_REPORTER=true`
3. Check if `SENTRY_DSN` is set (disables internal)
4. Inspect browser console for reporter errors

### Support messages not received

1. Check `RECEIVING_EMAIL` env variable
2. Verify `RESEND_API_KEY` is set
3. Check rate limit (10/min per IP)
4. Look for email errors in backend logs

### Widget not showing

1. Verify `NEXT_PUBLIC_ENABLE_SUPPORT_WIDGET=true`
2. Check if `NEXT_PUBLIC_CRISP_WEBSITE_ID` is set (hides internal)
3. Clear browser cache
4. Check browser console for React errors

---

## Status

✅ **Implementation Complete**

- Backend endpoints: 4/4
- Frontend components: 2/2
- Error reporter: Auto-initialized
- Support widget: Ready to add to layout
- Documentation: This file
- Testing: Manual tests passing

**Next Steps:**
1. Add `<SupportWidget />` to layout
2. Test error reporting in browser
3. Send test support message
4. Monitor `logs/*.jsonl` files

**Costs:** $0 (uses existing Resend)  
**Switchover:** Automatic when vendor keys added  
**Maintenance:** None (fail-closed design)
