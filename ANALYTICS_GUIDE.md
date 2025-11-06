# Analytics & Metrics Tracking System

## Overview
The Levqor backend now includes a comprehensive analytics system for tracking user engagement on the marketing frontend.

## Backend Endpoints

### Track Events
```bash
POST /api/v1/metrics/track
Content-Type: application/json

{
  "type": "page_view|cta_click|newsletter|conversion",
  "payload": { "key": "value" },  # Optional metadata
  "ref": { "source": "..." }       # Optional referrer data
}

Response: {"ok": true, "id": "unique-metric-id"}
```

### Get Analytics Summary
```bash
GET /api/v1/metrics/summary

Response:
{
  "total": {
    "page_views": 100,
    "cta_clicks": 25,
    "newsletters": 10,
    "conversions": 5
  },
  "last_24h": { "page_views": 20, "cta_clicks": 5 },
  "last_7d": { "page_views": 80 },
  "by_day": {
    "2025-11-06": {
      "page_view": 10,
      "cta_click": 3
    }
  },
  "conversion_rate": 5.0,  # (conversions / page_views) * 100
  "cta_rate": 25.0,         # (cta_clicks / page_views) * 100
  "last_updated": 1762445011
}
```

## Frontend Integration

### Tracking Utility
The frontend includes a `logEvent()` utility in `src/utils/metrics.ts`:

```typescript
import { logEvent } from '@/utils/metrics';

// Track page view
logEvent('page_view', { path: '/' });

// Track CTA click
logEvent('cta_click', { plan: 'monthly' });

// Track newsletter signup
logEvent('newsletter', { email_hash: 'sha256-hash' });

// Track conversion
logEvent('conversion', { plan: 'annual', amount: 299 });
```

### Automatic Tracking
Events are automatically tracked in:
- **Page components**: On page load (useEffect)
- **CTA buttons**: On click events
- **Newsletter forms**: On successful signup
- **Pricing cards**: On plan selection

## Analytics Dashboard

### Access
Visit: `https://your-frontend.vercel.app/dashboard?token=<DASHBOARD_TOKEN>`

The dashboard requires a valid token matching the `DASHBOARD_TOKEN` environment variable.

### Features
- **Overview Cards**: Total metrics with 24h comparison
- **Performance Metrics**: CTR and conversion rate
- **7-Day Activity Table**: Daily breakdown by event type
- **Real-time Updates**: Data refreshed on every page load

### Configuration
Set in `.env.local`:
```bash
DASHBOARD_TOKEN=your-secret-token-here
NEXT_PUBLIC_BACKEND_BASE=https://api.levqor.ai
```

## Database Schema

```sql
CREATE TABLE metrics (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  payload TEXT,         -- JSON string
  ref TEXT,             -- JSON string
  timestamp REAL NOT NULL,
  created_at REAL
);

CREATE INDEX idx_metrics_type ON metrics(type);
CREATE INDEX idx_metrics_timestamp ON metrics(timestamp);
```

## Privacy & Security

- **PII Protection**: Email addresses are hashed (SHA-256) before storage
- **No Authentication Required**: `/api/v1/metrics/track` is public for frontend use
- **Dashboard Protected**: Requires token authentication
- **CORS Enabled**: Frontend can call backend from any domain

## Testing

```bash
# Track a test event
curl -X POST http://localhost:5000/api/v1/metrics/track \
  -H "Content-Type: application/json" \
  -d '{"type":"page_view","payload":{"path":"/test"}}'

# View summary
curl http://localhost:5000/api/v1/metrics/summary | jq

# Access dashboard
open "http://localhost:3000/dashboard?token=test"
```

## Deployment Notes

1. **Backend**: Already deployed to api.levqor.ai
2. **Frontend**: Deploy `levqor-web/` to Vercel (see `DEPLOYMENT.md`)
3. **Environment Variables**:
   - Backend: Set `DASHBOARD_TOKEN` in Replit secrets
   - Frontend: Set `NEXT_PUBLIC_BACKEND_BASE` and `DASHBOARD_TOKEN` in Vercel

## Metrics Insights

Current test data shows:
- ✅ Page views: 1
- ✅ CTA clicks: 1 (100% CTR)
- ✅ Newsletter signups: 1
- ✅ Conversions: 1 (100% conversion rate)

All endpoints are operational and tracking works end-to-end! 🎉
