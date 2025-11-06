# Support Chat Widget Integration

## Overview
Add live chat to reduce support load and improve user experience.

## Recommended: Crisp

### Why Crisp
- Free tier (2 seats)
- Clean UI
- Email fallback
- Mobile apps
- Chatbot support

### Setup (5 minutes)
1. Create account: https://crisp.chat
2. Get website ID from dashboard
3. Add to frontend:

```typescript
// levqor/frontend/src/app/layout.tsx
useEffect(() => {
  window.$crisp = [];
  window.CRISP_WEBSITE_ID = process.env.NEXT_PUBLIC_CRISP_WEBSITE_ID;
  
  (function(){
    const d = document;
    const s = d.createElement("script");
    s.src = "https://client.crisp.chat/l.js";
    s.async = 1;
    d.getElementsByTagName("head")[0].appendChild(s);
  })();
}, [])
```

4. Add env variable:
```
NEXT_PUBLIC_CRISP_WEBSITE_ID=your-website-id
```

### Features
- Live chat widget
- Offline messages → email
- Chat history
- File sharing
- Screen sharing (paid)

### Customization
```javascript
// Set user data
$crisp.push(["set", "user:email", [user.email]]);
$crisp.push(["set", "user:nickname", [user.name]]);
$crisp.push(["set", "session:data", [[
  ["credits", user.credits],
  ["plan", user.plan]
]]]);
```

## Alternative: Intercom

### Why Intercom
- Advanced features
- Product tours
- Help center
- Powerful automation

### Setup
```typescript
// Similar to Crisp
useEffect(() => {
  window.Intercom('boot', {
    app_id: process.env.NEXT_PUBLIC_INTERCOM_APP_ID,
    email: user.email,
    name: user.name,
    created_at: user.created_at
  });
}, [user])
```

### Cost
- **Free:** No (starts at $39/month)
- **Starter:** $39/seat/month
- **Pro:** $99/seat/month

## Cookie Consent Update

### Add to /legal/cookies
Update privacy policy to mention chat widgets:
- Crisp cookies: Session management
- Purpose: Support chat
- Duration: 6 months
- Opt-out: Disable chat widget

## Features Comparison

| Feature | Crisp Free | Crisp Pro | Intercom |
|---------|------------|-----------|----------|
| Live chat | ✅ | ✅ | ✅ |
| 2 seats | ✅ | Unlimited | Per seat |
| Email fallback | ✅ | ✅ | ✅ |
| Mobile apps | ✅ | ✅ | ✅ |
| Chatbots | ❌ | ✅ | ✅ |
| Product tours | ❌ | ❌ | ✅ |
| Help center | ❌ | ✅ | ✅ |
| **Cost** | $0 | $25/mo | $39+/mo |

## Recommendation
**Start with Crisp Free** (2 seats, $0/month)

Upgrade to Crisp Pro ($25/month) when you need:
- More than 2 support agents
- Chatbot automation
- Advanced triggers

Switch to Intercom ($99+/month) when you need:
- Product tours
- Advanced segmentation
- Help center

## Implementation Checklist
- [ ] Create Crisp/Intercom account
- [ ] Get website ID / app ID
- [ ] Add to frontend environment variables
- [ ] Install chat widget script
- [ ] Test on staging
- [ ] Update privacy policy
- [ ] Train support team

## Status
- ✅ Integration guide complete
- ✅ Code examples ready
- ⏳ Requires account creation (5 min)
