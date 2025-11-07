"""
Stripe Connect Payout Automation
Processes payouts to connected accounts for partner commissions
"""
import os
import requests
import sqlite3
from datetime import datetime

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
MIN_PAYOUT_AMOUNT = 5000  # $50.00 in cents

def get_pending_payouts() -> list:
    """Get partners eligible for payout"""
    conn = sqlite3.connect('levqor.db')
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, partner_code, stripe_account_id, pending_commission
        FROM partners
        WHERE pending_commission >= ? AND stripe_account_id IS NOT NULL
    """, (MIN_PAYOUT_AMOUNT / 100,))
    
    results = cur.fetchall()
    conn.close()
    
    return [
        {
            "partner_id": r[0],
            "partner_code": r[1],
            "stripe_account_id": r[2],
            "amount_cents": int(r[3] * 100)
        }
        for r in results
    ]

def create_payout(stripe_account_id: str, amount_cents: int, currency: str = "usd") -> dict:
    """
    Create Stripe payout to connected account
    
    Args:
        stripe_account_id: Stripe Connect account ID
        amount_cents: Payout amount in cents
        currency: Currency code
    
    Returns:
        Payout response or error dict
    """
    if not STRIPE_SECRET_KEY:
        return {"error": "STRIPE_SECRET_KEY not configured"}
    
    try:
        response = requests.post(
            "https://api.stripe.com/v1/payouts",
            auth=(STRIPE_SECRET_KEY, ""),
            data={
                "amount": str(amount_cents),
                "currency": currency,
                "stripe_account": stripe_account_id
            },
            timeout=10
        )
        
        return response.json()
    
    except Exception as e:
        return {"error": str(e)}

def record_payout(partner_id: int, amount: float, payout_id: str):
    """Record payout in database"""
    conn = sqlite3.connect('levqor.db')
    cur = conn.cursor()
    
    # Create payout record
    cur.execute("""
        INSERT INTO partner_payouts (partner_id, amount, payout_id, status)
        VALUES (?, ?, ?, 'completed')
    """, (partner_id, amount, payout_id))
    
    # Reset pending commission
    cur.execute("""
        UPDATE partners
        SET pending_commission = 0,
            total_paid = total_paid + ?
        WHERE id = ?
    """, (amount, partner_id))
    
    conn.commit()
    conn.close()

def process_payouts() -> dict:
    """
    Process all eligible payouts
    
    Returns:
        dict with processing results
    """
    print("[💰] Starting payout processing...")
    
    pending = get_pending_payouts()
    
    if not pending:
        print("[ℹ] No partners eligible for payout")
        return {"status": "no_payouts", "processed": 0}
    
    print(f"[📋] Found {len(pending)} partners eligible for payout")
    
    results = {
        "total": len(pending),
        "successful": 0,
        "failed": 0,
        "details": []
    }
    
    for partner in pending:
        partner_code = partner["partner_code"]
        amount_cents = partner["amount_cents"]
        amount_dollars = amount_cents / 100
        
        print(f"\n[→] Processing {partner_code}: ${amount_dollars:.2f}")
        
        payout_result = create_payout(
            partner["stripe_account_id"],
            amount_cents
        )
        
        if "error" in payout_result:
            print(f"[✗] Failed: {payout_result['error']}")
            results["failed"] += 1
            results["details"].append({
                "partner": partner_code,
                "status": "failed",
                "error": payout_result["error"]
            })
        else:
            payout_id = payout_result.get("id", "unknown")
            print(f"[✓] Success: {payout_id}")
            
            # Record in database
            record_payout(
                partner["partner_id"],
                amount_dollars,
                payout_id
            )
            
            results["successful"] += 1
            results["details"].append({
                "partner": partner_code,
                "status": "success",
                "payout_id": payout_id,
                "amount": amount_dollars
            })
    
    print(f"\n[📊] Payout Summary:")
    print(f"    Successful: {results['successful']}")
    print(f"    Failed: {results['failed']}")
    
    return results

if __name__ == "__main__":
    import json
    result = process_payouts()
    print(f"\n{json.dumps(result, indent=2)}")
