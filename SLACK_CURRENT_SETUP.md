# ✅ Current Slack Webhook Setup (2025 Method)

## 🚀 Step-by-Step (2 minutes)

### Step 1: Create Slack App
1. Go to: **https://api.slack.com/apps**
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Enter:
   - **App Name**: `Levqor` (or any name you like)
   - **Workspace**: Select your Slack workspace
5. Click **"Create App"**

### Step 2: Enable Incoming Webhooks
1. In the left sidebar, click **"Incoming Webhooks"** (under Features)
2. Toggle the switch at the top to **ON** (Activate Incoming Webhooks)

### Step 3: Add Webhook to Workspace
1. Scroll down to **"Webhook URLs for Your Workspace"**
2. Click **"Add New Webhook to Workspace"**
3. Select a channel (like #general or create #levqor-alerts)
4. Click **"Allow"**

### Step 4: Copy Your Webhook URL
You'll see your webhook URL appear:
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
```

Click the **"Copy"** button next to it.

### Step 5: Add to Replit Secrets
1. In Replit, open **Tools** panel (left sidebar)
2. Click **"Secrets"** (🔒 lock icon)
3. Click **"+ New Secret"**
4. Key: `SLACK_WEBHOOK_URL`
5. Value: Paste your webhook URL
6. Click **"Add Secret"**

✅ **Done!** Works immediately, no restart needed.

---

## ✅ Test It

```bash
curl -X POST http://localhost:5000/actions/slack.send \
  -H "Content-Type: application/json" \
  -d '{"text":"✅ Levqor Slack connector is working!"}'
```

Check your Slack channel - you should see the message!

---

## 🆘 Troubleshooting

**Problem**: "Can't find Incoming Webhooks in sidebar"
- **Solution**: Make sure you clicked "Features" to expand the menu

**Problem**: "Don't have permission to create apps"
- **Solution**: Ask your Slack workspace admin to create the app, or they can give you app creation permissions

**Problem**: "Webhook URL not showing up"
- **Solution**: Make sure the toggle is ON, then scroll down to "Webhook URLs for Your Workspace"

**Problem**: Getting 404 error when testing
- **Solution**: Double-check you copied the entire URL including `https://`

---

## 📚 Official Slack Docs
https://api.slack.com/messaging/webhooks
