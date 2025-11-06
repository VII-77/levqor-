#!/bin/bash
# D3 UPTIME MONITORING CONFIGURATION
# ==================================

# OPTION 1: UptimeRobot API Setup (Requires API key)
# ---------------------------------------------------
# Get your API key from: https://uptimerobot.com/dashboard#mySettings
# Then use these curl commands to create monitors:

UPTIMEROBOT_API_KEY="YOUR_API_KEY_HERE"

# Create Backend Monitor (/ready endpoint)
curl -X POST https://api.uptimerobot.com/v2/newMonitor \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "api_key=${UPTIMEROBOT_API_KEY}" \
  -d "friendly_name=Levqor Backend /ready" \
  -d "url=https://api.levqor.ai/ready" \
  -d "type=1" \
  -d "interval=300"

# Create Frontend Monitor
curl -X POST https://api.uptimerobot.com/v2/newMonitor \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "api_key=${UPTIMEROBOT_API_KEY}" \
  -d "friendly_name=Levqor Frontend" \
  -d "url=https://app.levqor.ai/" \
  -d "type=1" \
  -d "interval=300"


# OPTION 2: Cron-Based Monitoring (Self-Hosted)
# ----------------------------------------------
# Add these lines to your crontab (crontab -e):

# Check backend every 5 minutes
*/5 * * * * curl -f -s -o /dev/null -w "\%{http_code}" https://api.levqor.ai/ready | grep -q "200" || echo "Backend down at $(date)" >> /var/log/levqor_uptime.log

# Check frontend every 5 minutes  
*/5 * * * * curl -f -s -o /dev/null -w "\%{http_code}" https://app.levqor.ai/ | grep -q "200" || echo "Frontend down at $(date)" >> /var/log/levqor_uptime.log


# OPTION 3: Simple Shell Script Monitor
# --------------------------------------
# Save as monitor.sh and run in background or via cron

monitor_endpoint() {
  local name=$1
  local url=$2
  
  response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  
  if [ "$response" = "200" ]; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ✓ $name OK (HTTP $response)"
  else
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ✗ $name FAILED (HTTP $response)"
    # Add alerting here (email, Slack, PagerDuty, etc.)
  fi
}

# Run checks every 5 minutes
while true; do
  monitor_endpoint "Backend" "https://api.levqor.ai/ready"
  monitor_endpoint "Frontend" "https://app.levqor.ai/"
  sleep 300
done
