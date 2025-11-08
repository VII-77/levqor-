#!/usr/bin/env python3
"""
Predictive Cost Engine - Forecasts 30-day infrastructure costs
"""
import os
import sys
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("cost_predict")

def get_stripe_charges_last_30d() -> float:
    """Fetch Stripe charges from last 30 days"""
    stripe_key = os.environ.get("STRIPE_SECRET_KEY")
    if not stripe_key:
        log.warning("STRIPE_SECRET_KEY not set, using estimate")
        return 0.0
    
    try:
        url = "https://api.stripe.com/v1/charges"
        created_after = int((datetime.utcnow() - timedelta(days=30)).timestamp())
        
        response = requests.get(
            url,
            auth=(stripe_key, ""),
            params={"created[gte]": created_after, "limit": 100},
            timeout=10
        )
        
        if response.status_code == 200:
            charges = response.json().get("data", [])
            total = sum(c.get("amount", 0) for c in charges if c.get("paid")) / 100
            return total
        else:
            log.warning(f"Stripe API returned {response.status_code}")
            return 0.0
    except Exception as e:
        log.warning(f"Failed to fetch Stripe data: {e}")
        return 0.0

def estimate_infra_costs() -> Dict[str, float]:
    """Estimate infrastructure costs (Replit, Redis, etc.)"""
    replit_monthly = 20.0
    redis_monthly = float(os.environ.get("REDIS_MONTHLY_COST", 0))
    
    return {
        "replit": replit_monthly,
        "redis": redis_monthly,
        "vercel": 0.0,
        "sentry": 0.0
    }

def estimate_openai_usage() -> float:
    """Estimate OpenAI usage from recent activity"""
    try:
        import sqlite3
        db_path = os.environ.get("SQLITE_PATH", "levqor.db")
        if not os.path.exists(db_path):
            return 0.0
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cutoff = (datetime.utcnow() - timedelta(days=30)).isoformat()
        cursor.execute("SELECT COUNT(*) FROM users WHERE created_at > ?", (cutoff,))
        recent_users = cursor.fetchone()[0]
        conn.close()
        
        return recent_users * 0.05
    except Exception as e:
        log.warning(f"Failed to estimate OpenAI usage: {e}")
        return 0.0

def forecast_next_30d(
    stripe_last_30d: float,
    infra_costs: Dict[str, float],
    openai_estimate: float
) -> Dict[str, Any]:
    """
    Generate 30-day cost forecast
    
    Uses simple linear trend + 20% buffer for confidence range
    """
    total_last_30d = (
        stripe_last_30d +
        sum(infra_costs.values()) +
        openai_estimate
    )
    
    forecast_base = total_last_30d
    confidence_buffer = total_last_30d * 0.20
    
    return {
        "forecast_next_30d": round(forecast_base, 2),
        "confidence_low": round(forecast_base - confidence_buffer, 2),
        "confidence_high": round(forecast_base + confidence_buffer, 2),
        "breakdown": {
            "stripe_revenue_last_30d": round(stripe_last_30d, 2),
            "infra_costs": {k: round(v, 2) for k, v in infra_costs.items()},
            "openai_estimate": round(openai_estimate, 2),
            "total_cost_last_30d": round(total_last_30d, 2)
        },
        "computed_at": datetime.utcnow().isoformat()
    }

def persist_forecast(forecast: Dict[str, Any]) -> bool:
    """Save forecast to last_forecast.json"""
    try:
        with open("config/last_forecast.json", 'w') as f:
            json.dump(forecast, f, indent=2)
        return True
    except Exception as e:
        log.error(f"Failed to persist forecast: {e}")
        return False

def load_cached_forecast() -> Dict[str, Any]:
    """Load cached forecast if available and recent"""
    try:
        if os.path.exists("config/last_forecast.json"):
            with open("config/last_forecast.json", 'r') as f:
                forecast = json.load(f)
                
                computed_at = datetime.fromisoformat(forecast["computed_at"])
                age_hours = (datetime.utcnow() - computed_at).total_seconds() / 3600
                
                if age_hours < 24:
                    return forecast
    except Exception as e:
        log.warning(f"Failed to load cached forecast: {e}")
    
    return None

def main():
    """Main cost prediction routine"""
    try:
        log.info("🔍 Computing cost forecast...")
        
        persist = "--persist" in sys.argv
        
        stripe_charges = get_stripe_charges_last_30d()
        infra = estimate_infra_costs()
        openai = estimate_openai_usage()
        
        forecast = forecast_next_30d(stripe_charges, infra, openai)
        
        log.info(f"✅ Forecast complete: ${forecast['forecast_next_30d']:.2f} "
                f"(range: ${forecast['confidence_low']:.2f} - ${forecast['confidence_high']:.2f})")
        
        if persist:
            if persist_forecast(forecast):
                log.info("💾 Forecast persisted to config/last_forecast.json")
        
        print(json.dumps(forecast, indent=2))
        return 0
        
    except Exception as e:
        log.error(f"Cost prediction failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
