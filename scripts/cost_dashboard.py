"""
Cost Dashboard Aggregator
Collects cost metrics from various sources for unified monitoring
"""
import json
import requests
import os
from datetime import datetime
import sqlite3

def get_stripe_costs() -> dict:
    """Fetch Stripe balance and pending charges"""
    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    if not stripe_key:
        return {"error": "STRIPE_SECRET_KEY not configured"}
    
    try:
        # Get balance
        balance_response = requests.get(
            "https://api.stripe.com/v1/balance",
            auth=(stripe_key, ""),
            timeout=10
        )
        balance = balance_response.json()
        
        # Get recent charges (last 30 days)
        charges_response = requests.get(
            "https://api.stripe.com/v1/charges?limit=100",
            auth=(stripe_key, ""),
            timeout=10
        )
        charges = charges_response.json()
        
        total_revenue = sum(
            charge["amount"] / 100
            for charge in charges.get("data", [])
            if charge.get("status") == "succeeded"
        )
        
        return {
            "available_balance": balance.get("available", [{"amount": 0}])[0]["amount"] / 100,
            "pending_balance": sum(p["amount"] for p in balance.get("pending", [])) / 100,
            "currency": balance.get("available", [{"currency": "usd"}])[0].get("currency", "usd").upper(),
            "total_revenue_30d": total_revenue
        }
    
    except Exception as e:
        return {"error": str(e)}

def get_openai_costs() -> dict:
    """Estimate OpenAI API costs (based on usage tracking)"""
    # This is an estimate - OpenAI doesn't provide direct cost API
    # Track usage in your application and calculate based on pricing
    
    try:
        conn = sqlite3.connect('levqor.db')
        cur = conn.cursor()
        
        # Check if we have a cost tracking table
        cur.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='ai_usage_costs'
        """)
        
        if cur.fetchone():
            cur.execute("""
                SELECT SUM(cost) as total_cost
                FROM ai_usage_costs
                WHERE created_at > datetime('now', '-30 days')
            """)
            result = cur.fetchone()
            total_cost = result[0] if result and result[0] else 0.0
        else:
            total_cost = 0.0
        
        conn.close()
        
        return {
            "estimated_cost_30d": total_cost,
            "note": "Estimated from usage tracking"
        }
    
    except Exception as e:
        return {"error": str(e), "estimated_cost_30d": 0.0}

def get_database_metrics() -> dict:
    """Get database size and key metrics"""
    try:
        import os
        db_path = 'levqor.db'
        
        if os.path.exists(db_path):
            size_bytes = os.path.getsize(db_path)
            size_mb = size_bytes / (1024 * 1024)
            
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            
            # Get table counts
            cur.execute("SELECT COUNT(*) FROM users")
            users = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM partners")
            partners = cur.fetchone()[0]
            
            cur.execute("SELECT SUM(pending_commission) FROM partners")
            pending = cur.fetchone()[0] or 0.0
            
            conn.close()
            
            return {
                "size_mb": round(size_mb, 2),
                "total_users": users,
                "total_partners": partners,
                "pending_commissions": round(pending, 2)
            }
        else:
            return {"error": "Database not found"}
    
    except Exception as e:
        return {"error": str(e)}

def get_infrastructure_costs() -> dict:
    """Estimate infrastructure costs"""
    # These are typical costs - adjust based on actual usage
    costs = {
        "replit_autoscale": 0,  # Usage-based
        "redis_upstash": 10,  # ~$10/month for hobby tier
        "postgresql_neon": 0,  # Free tier or ~$10/month
        "resend_email": 0,  # First 3000 emails free
        "estimated_monthly": 10 + 10  # Redis + possible Postgres
    }
    
    return costs

def generate_cost_dashboard() -> dict:
    """
    Generate comprehensive cost dashboard
    
    Returns:
        dict with all cost metrics
    """
    dashboard = {
        "generated_at": datetime.utcnow().isoformat(),
        "stripe": get_stripe_costs(),
        "openai": get_openai_costs(),
        "database": get_database_metrics(),
        "infrastructure": get_infrastructure_costs()
    }
    
    # Calculate totals
    stripe_pending = abs(dashboard["stripe"].get("pending_balance", 0))
    openai_cost = dashboard["openai"].get("estimated_cost_30d", 0)
    infra_cost = dashboard["infrastructure"].get("estimated_monthly", 0)
    
    dashboard["summary"] = {
        "total_estimated_monthly_cost": round(stripe_pending + openai_cost + infra_cost, 2),
        "revenue_30d": dashboard["stripe"].get("total_revenue_30d", 0),
        "net_30d": round(
            dashboard["stripe"].get("total_revenue_30d", 0) - (openai_cost + infra_cost),
            2
        ),
        "currency": "USD"
    }
    
    return dashboard

if __name__ == "__main__":
    dashboard = generate_cost_dashboard()
    
    print("="* 60)
    print("LEVQOR COST DASHBOARD")
    print("="* 60)
    print()
    
    # Stripe
    if "error" not in dashboard["stripe"]:
        print(f"💰 STRIPE")
        print(f"   Available: ${dashboard['stripe']['available_balance']:.2f}")
        print(f"   Pending: ${abs(dashboard['stripe']['pending_balance']):.2f}")
        print(f"   Revenue (30d): ${dashboard['stripe']['total_revenue_30d']:.2f}")
    
    print()
    
    # OpenAI
    print(f"🤖 OPENAI")
    print(f"   Estimated Cost (30d): ${dashboard['openai']['estimated_cost_30d']:.2f}")
    
    print()
    
    # Database
    if "error" not in dashboard["database"]:
        print(f"💾 DATABASE")
        print(f"   Size: {dashboard['database']['size_mb']} MB")
        print(f"   Users: {dashboard['database']['total_users']}")
        print(f"   Partners: {dashboard['database']['total_partners']}")
        print(f"   Pending Commissions: ${dashboard['database']['pending_commissions']:.2f}")
    
    print()
    
    # Infrastructure
    print(f"🖥️  INFRASTRUCTURE (Estimated Monthly)")
    print(f"   Redis: ${dashboard['infrastructure']['redis_upstash']:.2f}")
    print(f"   PostgreSQL: ${dashboard['infrastructure']['postgresql_neon']:.2f}")
    print(f"   Replit: Usage-based")
    print(f"   Total: ${dashboard['infrastructure']['estimated_monthly']:.2f}")
    
    print()
    print("="* 60)
    print(f"📊 SUMMARY (30 days)")
    print(f"   Total Costs: ${dashboard['summary']['total_estimated_monthly_cost']:.2f}")
    print(f"   Revenue: ${dashboard['summary']['revenue_30d']:.2f}")
    print(f"   Net: ${dashboard['summary']['net_30d']:.2f}")
    print("="* 60)
    
    # Output JSON for programmatic use
    with open("logs/cost_dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    
    print()
    print("[✓] Full dashboard saved to: logs/cost_dashboard.json")
