#!/bin/bash
# Quick script to add OAuth secrets to Vercel
# Usage: ./add_vercel_secrets.sh

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 ADD OAUTH SECRETS TO VERCEL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if we're in the right directory
if [ ! -d "levqor-site" ]; then
    echo "❌ Error: levqor-site directory not found"
    echo "   Run this script from the workspace root"
    exit 1
fi

cd levqor-site

# Function to add secret
add_secret() {
    local name=$1
    local value=$2
    
    if [ -z "$value" ]; then
        read -p "Enter $name: " value
    fi
    
    if [ -n "$value" ]; then
        echo "$value" | vercel env add "$name" production preview development 2>/dev/null || \
        echo "$value" | vercel env add "$name" production 2>/dev/null || \
        echo "⚠️  Failed to add $name (may already exist)"
    else
        echo "⚠️  Skipped $name (no value provided)"
    fi
}

echo "This will add OAuth secrets to your Vercel project."
echo "Press Enter to use default values, or type custom values."
echo ""

# Generate NEXTAUTH_SECRET if needed
if [ ! -f "/tmp/nextauth_secret.txt" ]; then
    openssl rand -base64 32 > /tmp/nextauth_secret.txt
fi
NEXTAUTH_SECRET=$(cat /tmp/nextauth_secret.txt)

echo "Adding NEXTAUTH_SECRET..."
add_secret "NEXTAUTH_SECRET" "$NEXTAUTH_SECRET"

echo "Adding NEXTAUTH_URL..."
add_secret "NEXTAUTH_URL" "https://levqor.ai"

echo "Adding NEXT_PUBLIC_API_URL..."
add_secret "NEXT_PUBLIC_API_URL" "https://api.levqor.ai"

if [ -n "$RESEND_API_KEY" ]; then
    echo "Adding RESEND_API_KEY..."
    add_secret "RESEND_API_KEY" "$RESEND_API_KEY"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Now add your OAuth credentials:"
echo ""

read -p "Enter GOOGLE_CLIENT_ID (or press Enter to skip): " GOOGLE_ID
if [ -n "$GOOGLE_ID" ]; then
    add_secret "GOOGLE_CLIENT_ID" "$GOOGLE_ID"
    read -p "Enter GOOGLE_CLIENT_SECRET: " GOOGLE_SECRET
    add_secret "GOOGLE_CLIENT_SECRET" "$GOOGLE_SECRET"
else
    echo "⚠️  Skipped Google OAuth credentials"
fi

echo ""
read -p "Enter MICROSOFT_CLIENT_ID (or press Enter to skip): " MS_ID
if [ -n "$MS_ID" ]; then
    add_secret "MICROSOFT_CLIENT_ID" "$MS_ID"
    read -p "Enter MICROSOFT_CLIENT_SECRET: " MS_SECRET
    add_secret "MICROSOFT_CLIENT_SECRET" "$MS_SECRET"
else
    echo "⚠️  Skipped Microsoft OAuth credentials"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Secrets added to Vercel!"
echo ""
echo "Next: Deploy your frontend"
echo "  git push origin main"
echo ""
