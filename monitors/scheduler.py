"""
Automated Task Scheduler - APScheduler integration for periodic jobs
"""
import os
import logging
import subprocess
from datetime import datetime

log = logging.getLogger("levqor.scheduler")

def run_retention_aggregation():
    """Daily retention metrics aggregation"""
    log.info("Running retention aggregation...")
    try:
        result = subprocess.run(
            ["python3", "scripts/aggregate_retention.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            log.info("✅ Retention aggregation complete")
        else:
            log.error(f"Retention aggregation failed: {result.stderr}")
    except Exception as e:
        log.error(f"Retention aggregation error: {e}")

def run_slo_watchdog():
    """Every 5 minutes SLO check"""
    from monitors.slo_watchdog import get_watchdog
    from monitors.incident_response import get_responder
    
    log.debug("Running SLO watchdog check...")
    try:
        watchdog = get_watchdog()
        result = watchdog.check_slo(p99_latency_ms=50, error_rate=0, availability=1.0)
        
        if result["should_trigger_recovery"]:
            log.warning("SLO breach detected, triggering recovery")
            responder = get_responder()
            responder.recover(error_rate=0.01, recent_failures=5, dry_run=False)
    except Exception as e:
        log.error(f"SLO watchdog error: {e}")

def run_daily_ops_summary():
    """Daily ops summary email"""
    log.info("Running daily ops summary...")
    try:
        result = subprocess.run(
            ["python3", "scripts/ops_summary.py", "--type", "daily"],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            log.info("✅ Daily ops summary sent")
        else:
            log.error(f"Ops summary failed: {result.stderr}")
    except Exception as e:
        log.error(f"Ops summary error: {e}")

def run_cost_prediction():
    """Weekly cost prediction"""
    log.info("Running cost prediction...")
    try:
        result = subprocess.run(
            ["python3", "scripts/cost_predict.py", "--persist"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            log.info("✅ Cost prediction complete")
        else:
            log.error(f"Cost prediction failed: {result.stderr}")
    except Exception as e:
        log.error(f"Cost prediction error: {e}")

def update_kv_costs():
    """Persist cost metrics to KV store (hourly)"""
    import sqlite3
    log.debug("Updating KV cost metrics...")
    
    def _kv_upsert(key, val):
        conn = sqlite3.connect('levqor.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO kv (key, value, updated_at) 
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET 
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
        """, (key, str(val)))
        conn.commit()
        conn.close()
    
    try:
        from scripts.cost_predict import load_cached_forecast
        forecast = load_cached_forecast()
        
        if forecast:
            breakdown = forecast.get('breakdown', {})
            _kv_upsert('openai_cost_30d', breakdown.get('openai_estimate', 0))
            _kv_upsert('infra_cost_30d', sum(breakdown.get('infra_costs', {}).values()))
            _kv_upsert('stripe_revenue_30d', breakdown.get('stripe_revenue_last_30d', 1))
            log.debug("✅ KV costs updated")
    except Exception as e:
        log.error(f"KV cost update failed: {e}")

def init_scheduler():
    """Initialize and start APScheduler"""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        
        scheduler = BackgroundScheduler()
        
        scheduler.add_job(
            run_retention_aggregation,
            CronTrigger(hour=0, minute=5, timezone='UTC'),
            id='retention_aggregation',
            name='Daily retention metrics',
            replace_existing=True
        )
        
        scheduler.add_job(
            run_slo_watchdog,
            'interval',
            minutes=5,
            id='slo_watchdog',
            name='SLO monitoring',
            replace_existing=True
        )
        
        scheduler.add_job(
            run_daily_ops_summary,
            CronTrigger(hour=9, minute=0, timezone='Europe/London'),
            id='daily_ops_summary',
            name='Daily ops report',
            replace_existing=True
        )
        
        scheduler.add_job(
            run_cost_prediction,
            CronTrigger(day_of_week='mon', hour=2, minute=10, timezone='UTC'),
            id='cost_prediction',
            name='Weekly cost forecast',
            replace_existing=True
        )
        
        scheduler.add_job(
            update_kv_costs,
            'interval',
            hours=1,
            id='kv_costs',
            name='Hourly KV cost sync',
            replace_existing=True
        )
        
        scheduler.start()
        log.info("✅ APScheduler initialized with 5 jobs")
        return scheduler
        
    except ImportError:
        log.warning("APScheduler not installed, automated tasks disabled")
        return None
    except Exception as e:
        log.error(f"Scheduler initialization failed: {e}")
        return None

_scheduler = None

def get_scheduler():
    """Get or initialize scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = init_scheduler()
    return _scheduler
