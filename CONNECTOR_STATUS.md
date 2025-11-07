# Levqor Connectors - Current Status

**Last Updated**: 2025-01-07

## ✅ Active Connectors (3/5)

### 1. Email (Resend) - ✅ OPERATIONAL
- **Status**: Configured via `RESEND_API_KEY`
- **Integration**: Manual API key
- **Test**: `curl -X POST http://localhost:5000/actions/email.send -H "Content-Type: application/json" -d '{"to":"test@example.com","subject":"Test","text":"Hello"}'`

### 2. Notion - ✅ OPERATIONAL  
- **Status**: Configured via Replit OAuth Integration
- **Integration**: Replit native connector (automatic token refresh)
- **Permissions**: Read/write access to workspace
- **Test**: Requires database_id from your Notion workspace

### 3. Google Sheets - ✅ OPERATIONAL
- **Status**: Configured via Replit OAuth Integration  
- **Integration**: Replit native connector (automatic token refresh)
- **Permissions**: Read/write spreadsheets
- **Test**: Pass `spreadsheet_id` in request body or set `GOOGLE_SHEETS_SPREADSHEET_ID` env var

---

## ❌ Pending Connectors (2/5)

### 4. Slack - ⏳ NEEDS SETUP
- **Status**: Not configured
- **Required**: `SLACK_WEBHOOK_URL`
- **How to get**:
  1. Visit https://api.slack.com/messaging/webhooks
  2. Create incoming webhook for your workspace
  3. Add URL to Replit Secrets as `SLACK_WEBHOOK_URL`

### 5. Telegram - ⏳ NEEDS SETUP  
- **Status**: Not configured
- **Required**: `TELEGRAM_BOT_TOKEN`
- **How to get**:
  1. Message @BotFather on Telegram
  2. Send `/newbot` and follow prompts
  3. Add token to Replit Secrets as `TELEGRAM_BOT_TOKEN`
  4. (Optional) Add `TELEGRAM_CHAT_ID_DEFAULT` for default recipient

---

## Quick Setup Commands

```bash
# Check current status
curl http://localhost:5000/actions/health

# Add Slack webhook
replit secrets set SLACK_WEBHOOK_URL 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

# Add Telegram bot token
replit secrets set TELEGRAM_BOT_TOKEN 'YOUR_BOT_TOKEN_HERE'

# Run setup helper
./scripts/setup_connectors.sh
```

---

## Integration Methods

| Connector | Method | Auto-Refresh | Setup Difficulty |
|-----------|--------|--------------|------------------|
| Email | Manual API Key | No | Easy |
| Notion | Replit OAuth | Yes ✅ | Click to connect |
| Google Sheets | Replit OAuth | Yes ✅ | Click to connect |
| Slack | Manual Webhook | N/A | Easy |
| Telegram | Manual API Key | No | Easy |

---

## API Endpoints

All connectors available at `/actions/*`:
- `POST /actions/email.send` ✅
- `POST /actions/notion.create` ✅
- `POST /actions/sheets.append` ✅
- `POST /actions/slack.send` ⏳
- `POST /actions/telegram.send` ⏳
- `GET /actions/health` (shows configuration status)

---

## Next Steps

1. **For Slack**: Get webhook URL from Slack and add to secrets
2. **For Telegram**: Create bot via @BotFather and add token to secrets

Both will work immediately after adding secrets (no code changes or restart needed).

---

See `docs/CONNECTORS.md` for full API documentation.
