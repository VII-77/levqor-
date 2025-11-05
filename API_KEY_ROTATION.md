# API Key Rotation Procedure

## Overview
Levqor backend supports zero-downtime API key rotation using a dual-key system.

## Environment Variables

- `API_KEYS`: Current active API keys (comma-separated)
- `API_KEYS_NEXT`: Next generation of API keys for rotation (comma-separated)

## Rotation Process

### Step 1: Add New Keys
Add your new keys to `API_KEYS_NEXT`:

```bash
API_KEYS=levqor_dev_abc123,levqor_dev_xyz789
API_KEYS_NEXT=levqor_new_000111,levqor_new_000222
```

Deploy and restart the service. Both old and new keys will be accepted.

### Step 2: Update Clients (24-48 hours)
During this window, update all API clients to use the new keys from `API_KEYS_NEXT`.

### Step 3: Promote New Keys
After all clients are updated, promote the new keys to `API_KEYS` and clear `API_KEYS_NEXT`:

```bash
API_KEYS=levqor_new_000111,levqor_new_000222
API_KEYS_NEXT=
```

Deploy and restart. Only the new keys will be accepted.

## Key Generation
Generate secure API keys using:

```bash
python3 -c "import secrets; print('levqor_' + secrets.token_urlsafe(16))"
```

## Security Best Practices

1. **Rotate Regularly**: Rotate keys every 90 days minimum
2. **Audit Usage**: Monitor API key usage via logs before rotation
3. **Secure Storage**: Store keys in secure environment variables, never in code
4. **Revoke Compromised**: If a key is compromised, rotate immediately
5. **Track Keys**: Maintain a secure audit log of which keys are assigned to which clients

## Emergency Revocation

If you need to revoke a key immediately:

1. Remove it from both `API_KEYS` and `API_KEYS_NEXT`
2. Deploy and restart immediately
3. Contact affected clients to provide new keys

## Monitoring

Check logs for authentication failures:

```bash
grep "forbidden" /tmp/logs/levqor-backend*.log
```

## Development Mode

When `API_KEYS` is not set or empty, the backend allows all requests (development only).
**Never deploy to production without setting API_KEYS.**
