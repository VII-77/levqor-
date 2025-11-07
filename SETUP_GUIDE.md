# Quick Connector Setup Guide

## 🎯 Setup Slack Connector (2 minutes)

### Step 1: Create Slack Webhook
1. Open in browser: **https://api.slack.com/messaging/webhooks**
2. Click **"Create your Slack app"**
3. Choose **"From scratch"**
4. Give it a name: `Levqor Notifications`
5. Select your Slack workspace

### Step 2: Enable Incoming Webhooks
1. In your app settings, click **"Incoming Webhooks"**
2. Toggle **ON** the "Activate Incoming Webhooks" switch
3. Click **"Add New Webhook to Workspace"**
4. Choose a channel (e.g., #general or create #levqor-alerts)
5. Click **"Allow"**

### Step 3: Copy Your Webhook URL
You'll see a webhook URL that looks like:
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
```

### Step 4: Add to Replit Secrets
1. In Replit, open the **Tools** panel (left sidebar)
2. Click **"Secrets"** (lock icon 🔒)
3. Click **"+ New Secret"**
4. Key: `SLACK_WEBHOOK_URL`
5. Value: Paste your webhook URL
6. Click **"Add Secret"**

✅ **Done!** Test it with:
```bash
curl -X POST http://localhost:5000/actions/slack.send \
  -H "Content-Type: application/json" \
  -d '{"text":"🎉 Levqor Slack connector is working!"}'
```

---

## 📱 Setup Telegram Connector (2 minutes)

### Step 1: Create Telegram Bot
1. Open **Telegram** app (mobile or desktop)
2. Search for: **@BotFather**
3. Start a chat and send: `/newbot`

### Step 2: Follow BotFather's Instructions
1. BotFather will ask: "Alright, a new bot. How are we going to call it?"
   - Enter a display name: `Levqor Alerts Bot`

2. BotFather will ask: "Good. Now let's choose a username for your bot."
   - Enter a username: `levqor_alerts_bot` (must end with 'bot')

### Step 3: Copy Your Bot Token
BotFather will respond with:
```
Done! Congratulations on your new bot...
Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567
```

Copy that entire token!

### Step 4: Add to Replit Secrets
1. In Replit, open **Tools** → **Secrets** (🔒)
2. Click **"+ New Secret"**
3. Key: `TELEGRAM_BOT_TOKEN`
4. Value: Paste your bot token
5. Click **"Add Secret"**

### Step 5: Get Your Chat ID (Optional but Recommended)
1. In Telegram, send a message to your new bot (any message)
2. Visit in browser: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for `"chat":{"id":123456789}`
4. Copy that chat ID number

### Step 6: Add Chat ID to Secrets (Optional)
1. In Replit Secrets, click **"+ New Secret"**
2. Key: `TELEGRAM_CHAT_ID_DEFAULT`
3. Value: Paste your chat ID
4. Click **"Add Secret"**

✅ **Done!** Test it with:
```bash
# If you added TELEGRAM_CHAT_ID_DEFAULT:
curl -X POST http://localhost:5000/actions/telegram.send \
  -H "Content-Type: application/json" \
  -d '{"text":"🚀 Levqor Telegram connector is working!"}'

# Or specify chat_id in request:
curl -X POST http://localhost:5000/actions/telegram.send \
  -H "Content-Type: application/json" \
  -d '{"text":"🚀 It works!","chat_id":"YOUR_CHAT_ID"}'
```

---

## ✅ Verify All Connectors

After setup, check status:
```bash
curl http://localhost:5000/actions/health
```

You should see:
```json
{
  "configured": 5,
  "connectors": {
    "email": true,
    "notion": true,
    "sheets": true,
    "slack": true,
    "telegram": true
  }
}
```

---

## 🎉 You're All Set!

All 5 connectors are now ready to use. See `docs/CONNECTORS.md` for full API documentation.
