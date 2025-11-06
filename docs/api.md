# Levqor API Reference

Complete API documentation for the Levqor backend.

## Base URL

```
https://api.levqor.ai
```

## Authentication

API keys are required for all write operations (POST, PATCH). Include your key in the `X-Api-Key` header:

```bash
X-Api-Key: your-api-key-here
```

## Rate Limits

- **Per-IP**: 20 requests/minute
- **Global**: 200 requests/minute

Rate limit headers are included in all responses:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`
- `Retry-After` (when rate limited)

---

## Endpoints

### Health & Metrics

#### `GET /`
Root health check endpoint.

**Response:**
```json
{
  "ok": true,
  "service": "levqor-backend",
  "version": "1.0.0",
  "build": "2025-11-06.1"
}
```

#### `GET /health`
Public health check.

**Response:**
```json
{
  "ok": true,
  "ts": 1699276800
}
```

#### `GET /public/metrics`
Public metrics dashboard.

**Response:**
```json
{
  "uptime_rolling_7d": 99.99,
  "jobs_today": 1250,
  "audit_coverage": 100,
  "last_updated": 1699276800
}
```

---

### Job Management

#### `POST /api/v1/intake`
Submit a new job for processing.

**Authentication:** Required

**Request:**
```json
{
  "workflow": "ai-analysis",
  "payload": {
    "input": "data"
  },
  "callback_url": "https://your-app.com/webhook",
  "priority": "normal"
}
```

**Fields:**
- `workflow` (string, required): Workflow identifier (1-128 chars)
- `payload` (object, required): Job data (max 200KB)
- `callback_url` (string, optional): HTTP(S) callback URL (1-1024 chars)
- `priority` (string, optional): `low`, `normal`, or `high`

**Response (202 Accepted):**
```json
{
  "job_id": "a1b2c3d4e5f6",
  "status": "queued"
}
```

#### `GET /api/v1/status/{job_id}`
Check job status.

**Response:**
```json
{
  "job_id": "a1b2c3d4e5f6",
  "status": "succeeded",
  "created_at": 1699276800,
  "result": {
    "output": "processed data"
  },
  "error": null
}
```

**Status values:**
- `queued`: Job accepted, waiting for processing
- `running`: Job currently executing
- `succeeded`: Job completed successfully
- `failed`: Job failed with error

---

### User Management

#### `POST /api/v1/users/upsert`
Create or update a user (idempotent).

**Authentication:** Required

**Request:**
```json
{
  "email": "user@example.com",
  "name": "Jane Doe",
  "locale": "en-US",
  "currency": "USD",
  "meta": {
    "plan": "pro",
    "credits": 1000
  }
}
```

**Response (201 Created or 200 OK):**
```json
{
  "created": true,
  "user": {
    "id": "user123",
    "email": "user@example.com",
    "name": "Jane Doe",
    "locale": "en-US",
    "currency": "USD",
    "meta": {"plan": "pro", "credits": 1000},
    "created_at": 1699276800,
    "updated_at": 1699276800
  }
}
```

#### `GET /api/v1/users?email={email}`
Lookup user by email.

**Response:**
```json
{
  "id": "user123",
  "email": "user@example.com",
  ...
}
```

#### `GET /api/v1/users/{user_id}`
Get user by ID.

#### `PATCH /api/v1/users/{user_id}`
Update user fields.

**Authentication:** Required

---

### Connectors

#### `POST /api/v1/connect/{name}`
Execute connector task.

**Authentication:** Required

**Supported connectors:** `gmail`, `notion`, `slack`, `telegram`

**Request (Gmail example):**
```json
{
  "action": "list_labels",
  "credentials": {
    "token": "oauth2-token",
    "refresh_token": "...",
    "client_id": "...",
    "client_secret": "..."
  },
  "params": {}
}
```

**Response:**
```json
{
  "status": "ok",
  "connector": "gmail",
  "result": {
    "labels": ["INBOX", "SENT", "DRAFTS"]
  }
}
```

See [Connectors Guide](connectors) for detailed documentation.

---

### Billing

#### `POST /billing/create-checkout-session`
Create Stripe checkout session.

**Request:**
```json
{
  "price_id": "price_1234567890",
  "email": "user@example.com",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "sessionId": "cs_test_...",
  "url": "https://checkout.stripe.com/..."
}
```

#### `POST /billing/webhook`
Stripe webhook handler (internal use).

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "invalid_request",
  "details": "workflow field is required"
}
```

### 403 Forbidden
```json
{
  "error": "forbidden"
}
```

### 404 Not Found
```json
{
  "error": "not_found",
  "job_id": "xyz123"
}
```

### 429 Too Many Requests
```json
{
  "error": "rate_limited"
}
```

Headers include:
- `Retry-After: 60`
- `X-RateLimit-Reset: 1699276860`

### 500 Internal Server Error
```json
{
  "error": "internal_error"
}
```

---

## Security

- **HTTPS Only**: All API traffic encrypted
- **HSTS**: Strict-Transport-Security enforced
- **CSP**: Content-Security-Policy headers
- **API Keys**: Secure authentication
- **Rate Limiting**: DDoS protection
- **Input Validation**: JSON schema validation

---

## OpenAPI Specification

Full OpenAPI 3.0 spec available at:
```
GET /public/openapi.json
```
