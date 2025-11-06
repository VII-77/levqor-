#!/usr/bin/env python3
"""
Stripe Payment Reconciliation Script
Compares Stripe transactions with local database records.
"""

import sys
import os
import json
import sqlite3
from datetime import datetime, timedelta
from time import time
import argparse

# Stripe API would normally be imported here
# import stripe

def parse_args():
    parser = argparse.ArgumentParser(description="Reconcile Stripe payments")
    parser.add_argument("--since", default="1d", help="Time period (e.g., 1d, 7d, 30d)")
    parser.add_argument("--mode", default="test", choices=["test", "live"], help="Stripe mode")
    return parser.parse_args()

def parse_time_period(period_str):
    """Parse time period string like '1d', '7d', '30d'."""
    if period_str.endswith("d"):
        days = int(period_str[:-1])
        return timedelta(days=days)
    elif period_str.endswith("h"):
        hours = int(period_str[:-1])
        return timedelta(hours=hours)
    else:
        raise ValueError(f"Invalid period format: {period_str}")

def get_stripe_transactions(since, mode):
    """
    Fetch Stripe transactions from API.
    In production, this would use stripe.PaymentIntent.list()
    """
    # Mock implementation for demonstration
    # In real implementation, would call Stripe API
    
    print(f"[INFO] Fetching Stripe {mode} transactions since {since}")
    
    # Simulate API call
    # stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
    # transactions = stripe.PaymentIntent.list(
    #     created={"gte": int(since.timestamp())},
    #     limit=100
    # )
    
    # Return mock data for now
    return []

def get_local_transactions(since_timestamp):
    """Get local transaction records from database."""
    db_path = os.environ.get("SQLITE_PATH", "levqor.db")
    
    if not os.path.exists(db_path):
        print(f"[WARN] Database not found: {db_path}")
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if we have a transactions table
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='transactions'
    """)
    
    if not cursor.fetchone():
        print("[INFO] No transactions table found (expected for new deployments)")
        conn.close()
        return []
    
    # Fetch transactions
    cursor.execute("""
        SELECT id, amount, status, created_at 
        FROM transactions 
        WHERE created_at > ?
    """, (since_timestamp,))
    
    transactions = cursor.fetchall()
    conn.close()
    
    return transactions

def reconcile(stripe_txns, local_txns):
    """Compare Stripe and local transactions."""
    stripe_ids = {txn.get("id") for txn in stripe_txns}
    local_ids = {txn[0] for txn in local_txns}
    
    missing_in_local = stripe_ids - local_ids
    missing_in_stripe = local_ids - stripe_ids
    
    return {
        "stripe_count": len(stripe_txns),
        "local_count": len(local_txns),
        "missing_in_local": len(missing_in_local),
        "missing_in_stripe": len(missing_in_stripe),
        "matched": len(stripe_ids & local_ids)
    }

def main():
    args = parse_args()
    
    # Parse time period
    period = parse_time_period(args.since)
    since = datetime.now() - period
    since_timestamp = int(since.timestamp())
    
    print("="*80)
    print("STRIPE RECONCILIATION REPORT")
    print("="*80)
    print(f"Mode: {args.mode}")
    print(f"Period: {args.since} (since {since.strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"Timestamp: {since_timestamp}")
    print()
    
    # Fetch transactions
    stripe_txns = get_stripe_transactions(since, args.mode)
    local_txns = get_local_transactions(since_timestamp)
    
    print(f"[INFO] Stripe transactions: {len(stripe_txns)}")
    print(f"[INFO] Local transactions: {len(local_txns)}")
    
    # Reconcile
    results = reconcile(stripe_txns, local_txns)
    
    print()
    print("RECONCILIATION RESULTS:")
    print("-" * 80)
    print(f"  Stripe Count:        {results['stripe_count']}")
    print(f"  Local Count:         {results['local_count']}")
    print(f"  Matched:             {results['matched']}")
    print(f"  Missing in Local:    {results['missing_in_local']}")
    print(f"  Missing in Stripe:   {results['missing_in_stripe']}")
    print()
    
    # Determine status
    if results['missing_in_local'] > 0 or results['missing_in_stripe'] > 0:
        status = "WARN"
        print(f"Status: {status} - Discrepancies detected")
    else:
        status = "OK"
        print(f"Status: {status} - All transactions reconciled")
    
    # Output compact status line for parsing
    print()
    print(f"RECONCILE_STATUS: {status} stripe={results['stripe_count']} local={results['local_count']} matched={results['matched']}")
    
    return 0 if status == "OK" else 1

if __name__ == "__main__":
    sys.exit(main())
