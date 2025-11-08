#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 AUTOMATED OAUTH SETUP FOR LEVQOR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Generate NEXTAUTH_SECRET
echo -e "${YELLOW}Step 1: Generating NEXTAUTH_SECRET...${NC}"
NEXTAUTH_SECRET=$(openssl rand -base64 32)
echo -e "${GREEN}✅ Generated: $NEXTAUTH_SECRET${NC}"
echo ""

# Step 2: Check if Vercel CLI is available
echo -e "${YELLOW}Step 2: Checking Vercel CLI...${NC}"
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel@latest
fi
echo -e "${GREEN}✅ Vercel CLI ready${NC}"
echo ""

# Step 3: Prepare environment variables file
echo -e "${YELLOW}Step 3: Creating OAuth credentials template...${NC}"
cat > /tmp/oauth_secrets.txt << EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 REQUIRED SECRETS FOR VERCEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXTAUTH_SECRET=$NEXTAUTH_SECRET
NEXTAUTH_URL=https://levqor.ai
NEXT_PUBLIC_API_URL=https://api.levqor.ai
RESEND_API_KEY=${RESEND_API_KEY}

# You need to add these after creating OAuth apps:
GOOGLE_CLIENT_ID=<from Google Console>
GOOGLE_CLIENT_SECRET=<from Google Console>
MICROSOFT_CLIENT_ID=<from Azure Portal>
MICROSOFT_CLIENT_SECRET=<from Azure Portal>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF

echo -e "${GREEN}✅ Secrets template created: /tmp/oauth_secrets.txt${NC}"
echo ""

# Step 4: Create OAuth app creation guide
cat > /tmp/oauth_quickstart.md << 'EOF'
# 🚀 OAuth Quick Setup Guide

## Google OAuth (5 minutes)
1. Visit: https://console.cloud.google.com/apis/credentials
2. Click: "Create Credentials" → "OAuth 2.0 Client ID"
3. Setup:
   - Type: Web application
   - Name: Levqor Production
   - Redirect URI: https://levqor.ai/api/auth/callback/google
4. Copy: Client ID and Client Secret

## Microsoft OAuth (5 minutes)
1. Visit: https://portal.azure.com
2. Search: "App registrations"
3. Click: "New registration"
4. Setup:
   - Name: Levqor Production
   - Accounts: Multitenant + personal Microsoft accounts
   - Redirect URI (Web): https://levqor.ai/api/auth/callback/azure-ad
5. Copy: Application (client) ID from overview page
6. Go to: "Certificates & secrets" → "New client secret"
7. Copy: Secret VALUE immediately (shown only once!)

## Add to Vercel
Run this command from levqor-site/ directory:

```bash
vercel env add NEXTAUTH_SECRET production
vercel env add NEXTAUTH_URL production
vercel env add GOOGLE_CLIENT_ID production
vercel env add GOOGLE_CLIENT_SECRET production
vercel env add MICROSOFT_CLIENT_ID production
vercel env add MICROSOFT_CLIENT_SECRET production
vercel env add RESEND_API_KEY production
vercel env add NEXT_PUBLIC_API_URL production
```

Or use Vercel Dashboard: https://vercel.com/dashboard
Settings → Environment Variables → Add each secret
EOF

echo -e "${GREEN}✅ Quick guide created: /tmp/oauth_quickstart.md${NC}"
echo ""

# Step 5: Interactive Vercel setup (if token available)
if [ -n "$VERCEL_TOKEN" ]; then
    echo -e "${YELLOW}Step 4: Setting up Vercel environment variables...${NC}"
    echo ""
    
    cd levqor-site
    
    # Set the guaranteed secrets first
    echo "Setting NEXTAUTH_SECRET..."
    echo "$NEXTAUTH_SECRET" | vercel env add NEXTAUTH_SECRET production --token="$VERCEL_TOKEN" || true
    
    echo "Setting NEXTAUTH_URL..."
    echo "https://levqor.ai" | vercel env add NEXTAUTH_URL production --token="$VERCEL_TOKEN" || true
    
    echo "Setting NEXT_PUBLIC_API_URL..."
    echo "https://api.levqor.ai" | vercel env add NEXT_PUBLIC_API_URL production --token="$VERCEL_TOKEN" || true
    
    if [ -n "$RESEND_API_KEY" ]; then
        echo "Setting RESEND_API_KEY..."
        echo "$RESEND_API_KEY" | vercel env add RESEND_API_KEY production --token="$VERCEL_TOKEN" || true
    fi
    
    echo -e "${GREEN}✅ Base secrets configured in Vercel${NC}"
    echo ""
    
    cd ..
else
    echo -e "${YELLOW}⚠️  VERCEL_TOKEN not set - skipping automated Vercel setup${NC}"
    echo ""
fi

# Final instructions
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ AUTOMATED SETUP COMPLETE${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Create OAuth apps (10 min total):"
echo "   - Google: https://console.cloud.google.com/apis/credentials"
echo "   - Microsoft: https://portal.azure.com"
echo "   See full guide: cat /tmp/oauth_quickstart.md"
echo ""
echo "2. Add OAuth credentials to Vercel:"
echo "   https://vercel.com/dashboard → Settings → Environment Variables"
echo ""
echo "   Add these 4 secrets:"
echo "   - GOOGLE_CLIENT_ID"
echo "   - GOOGLE_CLIENT_SECRET"
echo "   - MICROSOFT_CLIENT_ID"
echo "   - MICROSOFT_CLIENT_SECRET"
echo ""
echo "3. Deploy frontend:"
echo "   git add -A"
echo "   git commit -m 'OAuth setup complete'"
echo "   git push origin main"
echo ""
echo "4. Test authentication:"
echo "   Visit: https://levqor.ai/signin"
echo "   Test: Email magic links + Google + Microsoft login"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Your generated secrets are saved in: /tmp/oauth_secrets.txt"
echo ""
