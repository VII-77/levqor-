# How to Add Environment Variables & Deploy on Replit

## Step-by-Step Instructions

### 1️⃣ Open Deployments
1. In your Replit project, look at the left sidebar
2. Click the **"Deployments"** icon (rocket icon 🚀)

### 2️⃣ Create or Configure Deployment
- If this is your first deployment: Click **"Create Deployment"**
- If you already have a deployment: Click the **gear icon** ⚙️ to edit

### 3️⃣ Add Environment Variables

Look for the **"Environment Variables"** or **"Secrets"** section:

1. Click **"Add Variable"** or **"+"**
2. Add each variable:

   **First Variable:**
   ```
   Key:   API_KEYS
   Value: prod_key1,prod_key2
   ```
   (Replace with your actual production API keys, comma-separated)

   **Second Variable:**
   ```
   Key:   BUILD_ID
   Value: 2025-11-05.1
   ```

3. Click **"Save"** or **"Add"** for each variable

### 4️⃣ Verify Settings

Make sure these are correct:
- **Deployment Type:** Autoscale (should be already set)
- **Health Check Path:** `/` (should be already set)
- **Start Command:** Should be auto-configured

### 5️⃣ Deploy

1. Click the **"Deploy"** or **"Publish"** button
2. Wait for the deployment to complete (green checkmark ✅)
3. **Copy the deployment URL** - it will look like:
   - `your-app-name.repl.app` or
   - `deployment-name-username.repl.app`

### 6️⃣ Get Your Deployment URL

After deployment succeeds:
1. In the Deployments tab, you'll see your live deployment
2. Click to expand and see the URL
3. Copy this URL (you'll need it for DNS)

---

## ⚠️ Common Issues

**Can't find Environment Variables section?**
- Look for "Secrets" or "Environment" tab
- It's usually in the deployment configuration page

**Deployment fails?**
- Check that API_KEYS has no spaces around commas
- Verify both variables are added
- Check deployment logs for errors

**Need help?**
- The deployment logs will show any errors
- Come back with the error message and I'll help debug

---

## Next Steps After Deployment

Once deployed, you need to:

1. **Configure DNS:**
   ```
   CNAME  api.levqor.ai  →  <your-deployment-url-from-above>
   ```

2. **Deploy Frontend on Vercel:**
   ```
   VITE_API_URL=https://api.levqor.ai
   ```

3. **Run Smoke Tests** (after DNS propagates):
   ```bash
   ./smoke_test.sh <your-api-key>
   ```

---

Good luck with your deployment! 🚀
