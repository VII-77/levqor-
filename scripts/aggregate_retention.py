#!/usr/bin/env python3
"""
Retention Analytics Aggregator - Computes DAU/WAU/MAU from user activity
"""
import os
import sys
import sqlite3
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("aggregate_retention")

def get_db_path():
    """Get database path"""
    return os.environ.get("SQLITE_PATH", os.path.join(os.getcwd(), "levqor.db"))

def ensure_analytics_table(conn):
    """Create analytics_aggregates table if not exists"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analytics_aggregates (
            day DATE PRIMARY KEY,
            dau INTEGER NOT NULL DEFAULT 0,
            wau INTEGER NOT NULL DEFAULT 0,
            mau INTEGER NOT NULL DEFAULT 0,
            computed_at TEXT NOT NULL
        )
    """)
    conn.commit()

def compute_retention_metrics(conn, target_date=None):
    """Compute DAU/WAU/MAU for a specific date"""
    if target_date is None:
        target_date = datetime.utcnow().date()
    
    target_day = target_date.isoformat()
    week_ago = (target_date - timedelta(days=7)).isoformat()
    month_ago = (target_date - timedelta(days=30)).isoformat()
    
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(DISTINCT id) FROM users
        WHERE DATE(last_login_at) = ?
    """, (target_day,))
    dau = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT COUNT(DISTINCT id) FROM users
        WHERE DATE(last_login_at) >= ? AND DATE(last_login_at) <= ?
    """, (week_ago, target_day))
    wau = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT COUNT(DISTINCT id) FROM users
        WHERE DATE(last_login_at) >= ? AND DATE(last_login_at) <= ?
    """, (month_ago, target_day))
    mau = cursor.fetchone()[0] or 0
    
    return dau, wau, mau

def upsert_metrics(conn, target_date, dau, wau, mau):
    """Upsert daily metrics"""
    target_day = target_date.isoformat()
    computed_at = datetime.utcnow().isoformat()
    
    conn.execute("""
        INSERT INTO analytics_aggregates (day, dau, wau, mau, computed_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(day) DO UPDATE SET
            dau = excluded.dau,
            wau = excluded.wau,
            mau = excluded.mau,
            computed_at = excluded.computed_at
    """, (target_day, dau, wau, mau, computed_at))
    conn.commit()

def main():
    """Main aggregation routine"""
    try:
        db_path = get_db_path()
        if not os.path.exists(db_path):
            log.error(f"Database not found: {db_path}")
            return 1
        
        conn = sqlite3.connect(db_path)
        ensure_analytics_table(conn)
        
        today = datetime.utcnow().date()
        dau, wau, mau = compute_retention_metrics(conn, today)
        
        log.info(f"Computed metrics for {today}: DAU={dau}, WAU={wau}, MAU={mau}")
        
        upsert_metrics(conn, today, dau, wau, mau)
        
        conn.close()
        
        log.info("✅ Retention aggregation complete")
        return 0
        
    except Exception as e:
        log.error(f"Aggregation failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
