# Easiest Slack Setup Method

## 🚀 Super Simple Slack Webhook (30 seconds)

### Method 1: Use Slack Workflow Builder (EASIEST)

1. **Open Slack** on web/desktop
2. **Click your workspace name** (top left) → **Tools** → **Workflow Builder**
3. **Create** → **From Scratch**
4. **Name it**: "Levqor Alerts"
5. **Starts with**: Select **"Webhook"**
6. **Copy the webhook URL** that appears
7. **Add variable**: Skip this, just click **Publish**

**Add to Replit:**
- Go to Replit **Secrets** panel
- Add: `SLACK_WEBHOOK_URL` = your webhook URL
- Done! ✅

---

### Method 2: Quick Incoming Webhook App (Alternative)

If you don't have Workflow Builder:

1. **Go to**: https://my.slack.com/services/new/incoming-webhook
2. **Choose a channel** (like #general)
3. **Click "Add Incoming WebHooks integration"**
4. **Copy the Webhook URL**

**Add to Replit:**
- Replit **Secrets** panel
- Add: `SLACK_WEBHOOK_URL` = your webhook URL
- Done! ✅

---

### Method 3: Classic Slack App (Most Reliable)

1. Go to: **https://api.slack.com/apps**
2. Click **"Create New App"** → **"From scratch"**
3. Name: `Levqor`, select your workspace
4. Click **"Incoming Webhooks"** in left sidebar
5. Toggle **ON** at the top
6. Scroll down → **"Add New Webhook to Workspace"**
7. Choose #general → **Allow**
8. **Copy the webhook URL** (starts with `https://hooks.slack.com/...`)

**Add to Replit:**
- Replit **Secrets** panel  
- Key: `SLACK_WEBHOOK_URL`
- Value: Paste webhook URL
- ✅ Works instantly!

---

## ✅ Test After Adding

```bash
curl -X POST http://localhost:5000/actions/slack.send \
  -H "Content-Type: application/json" \
  -d '{"text":"✅ Slack connector works!"}'
```

---

## 🆘 Still Having Issues?

**Most common problems:**

1. **Webhook URL format**: Should start with `https://hooks.slack.com/services/`
2. **Copy the entire URL**: Don't miss any characters
3. **No spaces**: Make sure no spaces before/after in Secrets
4. **Workspace permissions**: Make sure you're an admin or have app install permissions

**Need help?** Tell me what error you're seeing and I'll fix it!
