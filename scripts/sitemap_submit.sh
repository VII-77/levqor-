#!/bin/bash
# Sitemap Auto-Submit
# Notifies search engines about sitemap updates

SITEMAP_URL="${SITEMAP_URL:-https://levqor.ai/sitemap.xml}"

echo "[🗺️] Submitting sitemap: $SITEMAP_URL"

# Submit to Google
echo "[→] Notifying Google..."
GOOGLE_RESPONSE=$(curl -s "https://www.google.com/ping?sitemap=$SITEMAP_URL")
echo "[✓] Google notified"

# Submit to Bing
echo "[→] Notifying Bing..."
BING_RESPONSE=$(curl -s "https://www.bing.com/ping?sitemap=$SITEMAP_URL")
echo "[✓] Bing notified"

# Optional: Submit to Yandex
if [ -n "$SUBMIT_YANDEX" ]; then
    echo "[→] Notifying Yandex..."
    curl -s "https://webmaster.yandex.com/ping?sitemap=$SITEMAP_URL" > /dev/null
    echo "[✓] Yandex notified"
fi

echo ""
echo "[✓] Sitemap submission complete"
echo "    Next update: Add this to cron for weekly submission"
echo "    0 0 * * 0 bash scripts/sitemap_submit.sh >> logs/sitemap.log 2>&1"
