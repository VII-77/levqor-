"""
Aggregate growth retention metrics by source and cohort.
Builds referral_retention table from growth_events.
"""
import sqlite3
import time
import datetime as dt
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("levqor.growth_retention")

def aggregate_growth_retention():
    """
    Aggregate daily retention metrics by source from growth_events.
    
    Creates daily snapshots of:
    - DAU (Daily Active Users)
    - WAU (Weekly Active Users) 
    - MAU (Monthly Active Users)
    - Paid conversions
    
    Analyzes last 30 days.
    """
    try:
        conn = sqlite3.connect("levqor.db")
        c = conn.cursor()
        
        today = dt.date.today()
        processed_count = 0
        
        for days_ago in range(0, 30):
            target_date = today - dt.timedelta(days=days_ago)
            day_str = target_date.isoformat()
            day_ts = int(time.mktime(target_date.timetuple()))
            
            # Get unique active users by source for this day
            c.execute("""
                SELECT source, COUNT(DISTINCT user_id) 
                FROM growth_events 
                WHERE event='active' 
                  AND DATE(ts, 'unixepoch') = ? 
                GROUP BY source
            """, [day_str])
            
            daily_activity = c.fetchall()
            
            for source, dau in daily_activity:
                if not source:
                    source = "direct"
                
                # Calculate WAU (7-day window ending on this day)
                week_start = day_ts - (7 * 86400)
                c.execute("""
                    SELECT COUNT(DISTINCT user_id)
                    FROM growth_events
                    WHERE source = ?
                      AND event = 'active'
                      AND ts >= ?
                      AND ts <= ?
                """, [source, week_start, day_ts + 86400])
                wau = c.fetchone()[0]
                
                # Calculate MAU (30-day window ending on this day)
                month_start = day_ts - (30 * 86400)
                c.execute("""
                    SELECT COUNT(DISTINCT user_id)
                    FROM growth_events
                    WHERE source = ?
                      AND event = 'active'
                      AND ts >= ?
                      AND ts <= ?
                """, [source, month_start, day_ts + 86400])
                mau = c.fetchone()[0]
                
                # Count paid conversions on this day
                c.execute("""
                    SELECT COUNT(*)
                    FROM growth_events
                    WHERE source = ?
                      AND event = 'paid'
                      AND DATE(ts, 'unixepoch') = ?
                      AND revenue_cents > 0
                """, [source, day_str])
                paid = c.fetchone()[0]
                
                # Upsert retention record
                c.execute("""
                    INSERT OR REPLACE INTO referral_retention
                    (day, source, cohort, dau, wau, mau, paid)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, [day_str, source, "by_source", dau, wau, mau, paid])
                
                processed_count += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ GROWTH_RETENTION=ok (processed {processed_count} source-day records)")
        print(f"✅ GROWTH_RETENTION=ok (processed {processed_count} records)")
        return True
        
    except Exception as e:
        logger.error(f"❌ GROWTH_RETENTION failed: {e}")
        print(f"❌ STEP FAILED: GROWTH_RETENTION - {e}")
        return False

if __name__ == "__main__":
    success = aggregate_growth_retention()
    sys.exit(0 if success else 1)
