# 🚀 Supabase Setup Guide for Levqor

## Quick Setup (2 Minutes)

### Step 1: Create Supabase Project

1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Enter:
   - **Name:** levqor
   - **Database Password:** (generate secure password - save it!)
   - **Region:** Choose closest to you
4. Click "Create new project" (takes ~2 minutes)

### Step 2: Get Your API Credentials

Once your project is created:

1. Click "Settings" (gear icon) in sidebar
2. Click "API" in the settings menu
3. You'll see three important values:

**Copy these to Replit Secrets:**

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGci.....
SUPABASE_SERVICE_ROLE_KEY=eyJhbGci.....
```

### Step 3: Add to Replit Secrets

**Backend (this Replit):**
1. Click "Tools" → "Secrets" in Replit
2. Add three secrets:
   - `SUPABASE_URL` = (paste URL)
   - `SUPABASE_SERVICE_ROLE_KEY` = (paste service_role key)
   - `JWT_AUDIENCE` = `supabase`

**Frontend (Vercel):**
1. Go to Vercel dashboard → Your project → Settings → Environment Variables
2. Add three variables:
   - `NEXT_PUBLIC_SUPABASE_URL` = (paste URL)
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = (paste anon key)
   - `NEXT_PUBLIC_BACKEND_BASE` = `https://api.levqor.ai`
   - `NEXT_PUBLIC_FRONTEND_URL` = `https://levqor-site.vercel.app`

### Step 4: Configure Supabase Auth

In your Supabase dashboard:

1. Go to "Authentication" → "Providers"
2. Enable "Email" provider (should be on by default)
3. Optional: Enable "Google" provider:
   - Get OAuth credentials from Google Cloud Console
   - Add redirect URL: `https://YOUR_PROJECT.supabase.co/auth/v1/callback`

4. Go to "Authentication" → "URL Configuration"
5. Add site URL: `https://levqor-site.vercel.app`
6. Add redirect URLs:
   - `https://levqor-site.vercel.app/dashboard`
   - `http://localhost:3000/dashboard` (for local development)

### Step 5: Deploy Frontend

```bash
cd levqor/frontend
npm install
npm run build

# Deploy to Vercel
npx vercel --prod
```

### Step 6: Restart Backend

1. In Replit, click "Run" or restart the workflow
2. Backend will now accept Supabase JWTs

---

## ✅ Verification Checklist

### Backend Tests
```bash
# Test auth endpoint (should return 401)
curl https://api.levqor.ai/api/v1/me/subscription

# Test event tracking
curl -X POST https://api.levqor.ai/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{"type":"test","meta":{"source":"setup"}}'

# Test metrics summary
curl https://api.levqor.ai/api/v1/metrics/summary
```

### Frontend Tests
1. Go to your frontend URL: `https://levqor-site.vercel.app/signup`
2. Enter your email
3. Check inbox for magic link
4. Click link → Should redirect to dashboard
5. Dashboard should show:
   - Your email
   - Usage stats (empty initially)
   - Referral link

### Referral Test
1. Get referral code from dashboard
2. Open incognito: `https://levqor-site.vercel.app/?ref=YOUR_CODE`
3. Sign up with different email
4. Check first account dashboard - should show 1 referral

---

## 🎯 What This Enables

### User Authentication
- ✅ Email magic links (passwordless)
- ✅ Google OAuth (if configured)
- ✅ JWT verification on backend
- ✅ Protected dashboard routes

### Referral System
- ✅ Automatic ref code generation
- ✅ Referral tracking with UTM params
- ✅ +20 credits for 2 successful referrals
- ✅ Referral status in dashboard

### Analytics
- ✅ Event tracking (page views, signups, CTAs)
- ✅ Metrics summary endpoint
- ✅ 7-day conversion tracking
- ✅ JSONL event storage

### User Dashboard
- ✅ View subscription status
- ✅ See usage stats (last 14 days)
- ✅ Get referral link
- ✅ Track referral rewards

---

## 🔧 Environment Variables Summary

### Backend (Replit Secrets)
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGci...
JWT_AUDIENCE=supabase
```

### Frontend (Vercel Environment Variables)
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci...
NEXT_PUBLIC_BACKEND_BASE=https://api.levqor.ai
NEXT_PUBLIC_FRONTEND_URL=https://levqor-site.vercel.app
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=levqor.ai (optional)
```

---

## 🐛 Troubleshooting

### "unauthorized" or "invalid_token"
- Check SUPABASE_URL is correct
- Verify JWT_AUDIENCE is set to "supabase"
- Ensure SUPABASE_SERVICE_ROLE_KEY is the service_role key, not anon key

### Magic link not sending
- Check Supabase dashboard → Authentication → Settings
- Verify email templates are enabled
- Check spam folder

### Frontend won't load
- Run `cd levqor/frontend && npm install`
- Check `.env.local` has all required vars
- Try `npm run dev` locally first

### Referrals not tracking
- Check browser console for errors
- Verify `?ref=CODE` in URL
- Check localStorage has `levqor_ref`

---

## 📊 Database Schema

### Tables Created Automatically:
- **users:** id, email, ref_code, credits_remaining
- **referrals:** id, referrer_user_id, referee_email, credited
- **usage_daily:** id, user_id, day, jobs_run, cost_saving
- **metrics:** id, type, payload, timestamp

### Indexes:
- users(email) - unique
- users(ref_code)
- referrals(referrer_user_id)
- referrals(referee_email)
- usage_daily(user_id, day) - unique

---

## 🎉 Success Criteria

✅ Backend accepts Supabase JWTs  
✅ Frontend signup flow works  
✅ Dashboard loads with user data  
✅ Referral links generate and track  
✅ Analytics events fire correctly  
✅ Robots.txt and sitemap accessible  

---

**Setup time:** 5-10 minutes  
**Cost:** $0 (Supabase free tier: 50K monthly active users)  
**Production ready:** Yes
