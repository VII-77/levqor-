#!/bin/bash
# Deployment checklist for api.levqor.ai custom domain

echo "🚀 LEVQOR DEPLOYMENT CHECKLIST"
echo "================================"
echo ""

echo "📋 PRE-DEPLOYMENT CHECKS"
echo ""

echo -n "1. Backend running locally? "
if curl -fsS http://localhost:5000/status > /dev/null 2>&1; then
    echo "✅ Yes"
else
    echo "❌ No - Start backend first!"
    exit 1
fi

echo -n "2. Smoke test passes locally? "
export BACKEND="http://localhost:5000"
if ./public_smoke.sh > /dev/null 2>&1; then
    echo "✅ Yes (10/10)"
else
    echo "⚠️  Run: export BACKEND='http://localhost:5000' && ./public_smoke.sh"
fi

echo -n "3. Stripe secrets configured? "
if [ ! -z "$STRIPE_SECRET_KEY" ]; then
    echo "✅ Yes"
else
    echo "⚠️  Set STRIPE_SECRET_KEY in Replit Secrets"
fi

echo -n "4. Deploy config exists? "
if [ -f ".replit" ] || grep -q "deployment_target" pyproject.toml 2>/dev/null; then
    echo "✅ Yes"
else
    echo "⚠️  Configure with deploy_config_tool"
fi

echo ""
echo "📦 DEPLOYMENT STEPS"
echo ""
echo "1. Click 'Deploy' button in Replit (top right)"
echo "2. Select deployment type: Autoscale"
echo "3. Click 'Deploy' and wait for completion"
echo ""

echo "🌐 CUSTOM DOMAIN STEPS"
echo ""
echo "1. In Replit Deployments > Settings > Click 'Link a domain'"
echo "2. Enter domain: api.levqor.ai"
echo "3. Copy the A record IP and TXT verification code"
echo "4. Add to your DNS (Cloudflare/registrar):"
echo "   - A record: api → [IP from Replit]"
echo "   - TXT record: _replit-challenge.api → [code from Replit]"
echo "5. ⚠️  Cloudflare users: Set proxy to 'DNS only' (gray cloud)"
echo "6. Wait 10-60 minutes for verification"
echo ""

echo "✅ VERIFICATION"
echo ""
echo "After domain shows 'Verified' in Replit:"
echo ""
echo "  export BACKEND='https://api.levqor.ai'"
echo "  ./public_smoke.sh"
echo ""
echo "Expected: ✅ ALL PUBLIC SMOKE TESTS PASSED! (10/10)"
echo ""

echo "📚 Full guide: CUSTOM_DOMAIN_SETUP_GUIDE.md"
