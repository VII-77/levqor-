# 🔧 Setting Up Monitoring - Step by Step

## 1. Sentry Error Tracking (Backend)

### Get Your Sentry DSN
1. Go to https://sentry.io and sign up (free tier: 5K errors/month)
2. Create a new project
3. Select **Python** / **Flask**
4. Copy your DSN (looks like: `https://abc123@o123.ingest.sentry.io/456`)

### Add to Replit Secrets
1. In your Replit project, click **Secrets** (🔒) in the left sidebar
2. Click **+ New Secret**
3. Add:
   - **Key:** `SENTRY_DSN`
   - **Value:** Your actual DSN from Sentry

### Install Sentry SDK
```bash
pip install sentry-sdk[flask]
```

### Verify It's Working
After restarting your backend, you should see in logs:
```
✅ Sentry error tracking initialized
```

**Test error capture:**
```bash
# Trigger a test error
curl https://api.levqor.ai/test-error

# Check Sentry dashboard - you should see the error!
```

---

## 2. Crisp Chat Widget (Frontend)

### Get Your Crisp Website ID
1. Go to https://crisp.chat and sign up (free tier: 2 seats)
2. Create a new website
3. Go to Settings → Website Settings
4. Copy your **Website ID** (looks like: `abc12345-1234-1234-1234-123456789abc`)

### Add to Replit Secrets
1. In Replit **Secrets** (🔒)
2. Add:
   - **Key:** `NEXT_PUBLIC_CRISP_WEBSITE_ID`
   - **Value:** Your Website ID from Crisp

### Update Frontend
The frontend code will automatically pick up the environment variable and load the Crisp widget.

If you need to manually add it:
```typescript
// levqor/frontend/src/app/layout.tsx or pages/_app.tsx
useEffect(() => {
  if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_CRISP_WEBSITE_ID) {
    window.$crisp = [];
    window.CRISP_WEBSITE_ID = process.env.NEXT_PUBLIC_CRISP_WEBSITE_ID;
    
    (function(){
      const d = document;
      const s = d.createElement("script");
      s.src = "https://client.crisp.chat/l.js";
      s.async = 1;
      d.getElementsByTagName("head")[0].appendChild(s);
    })();
  }
}, []);
```

### Verify It's Working
After deploying your frontend, you should see the Crisp chat bubble in the bottom-right corner of your website.

---

## 3. UptimeRobot (Free Monitoring)

### Setup (No Secrets Needed)
1. Go to https://uptimerobot.com and sign up (100% free)
2. Click **+ Add New Monitor**
3. Configure:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Levqor API
   - **URL:** `https://api.levqor.ai/health`
   - **Monitoring Interval:** 5 minutes
4. Add alert contacts (your email)
5. Click **Create Monitor**

### What You Get
- Email alerts when your API goes down
- Uptime percentage tracking
- Response time graphs
- Public status page (optional)

**No code changes needed!** UptimeRobot just pings your `/health` endpoint.

---

## 4. Verification Checklist

After setup, verify everything works:

### Backend Health
```bash
curl https://api.levqor.ai/health
# Should return: {"ok": true}
```

### Sentry Working
```bash
# Check backend logs for:
✅ Sentry error tracking initialized

# Or trigger test error and check Sentry dashboard
```

### Crisp Widget Loaded
- Visit your frontend
- Look for chat bubble in bottom-right
- Click it to test

### UptimeRobot Monitoring
- Check your email for "Monitor is UP" confirmation
- Visit UptimeRobot dashboard to see first ping

---

## 5. Costs

| Service | Free Tier | When to Upgrade |
|---------|-----------|-----------------|
| **Sentry** | 5K errors/month | >10K users → $26/mo |
| **Crisp** | 2 seats | >2 support agents → $25/mo |
| **UptimeRobot** | 50 monitors | Always free! |

**Total Monthly Cost (free tier):** $0

---

## 6. Troubleshooting

### Sentry Not Working
- ✅ Verify `SENTRY_DSN` is in Replit Secrets
- ✅ Check you installed: `pip install sentry-sdk[flask]`
- ✅ Restart backend workflow
- ✅ Check logs for initialization message

### Crisp Not Showing
- ✅ Verify `NEXT_PUBLIC_CRISP_WEBSITE_ID` is in Replit Secrets (must have `NEXT_PUBLIC_` prefix!)
- ✅ Rebuild frontend
- ✅ Clear browser cache
- ✅ Check browser console for errors

### UptimeRobot Not Pinging
- ✅ Verify URL is correct: `https://api.levqor.ai/health`
- ✅ Make sure backend is deployed and running
- ✅ Check monitor status in UptimeRobot dashboard

---

## Next Steps

Once monitoring is set up:
1. ✅ Watch Sentry for production errors
2. ✅ Respond to UptimeRobot downtime alerts
3. ✅ Use Crisp to chat with users
4. 📊 Review Sentry performance metrics weekly
5. 🎯 Fix top errors based on Sentry insights

**You now have production-grade monitoring!** 🎉
