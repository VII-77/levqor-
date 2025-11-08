"""
Auto-tuning engine for SLO and performance targets.
Analyzes historical metrics and suggests parameter adjustments.
"""
import time
import sqlite3
import logging
from typing import Dict, Any

logger = logging.getLogger("levqor.auto_tune")

def get_recent_metrics() -> Dict[str, float]:
    """Fetch last 7 days of performance metrics from KV store"""
    conn = sqlite3.connect("levqor.db")
    c = conn.cursor()
    
    # Get stored metrics
    c.execute("SELECT key, value FROM kv WHERE key LIKE '%_p95%' OR key LIKE '%queue%'")
    metrics = {k: float(v) for k, v in c.fetchall()}
    conn.close()
    
    return metrics

def compute_targets(observed_p95: float, observed_queue: int) -> Dict[str, int]:
    """
    Compute optimized targets based on observed performance.
    
    Algorithm:
    - P95 target: 80% of observed (min 40ms, max 150ms)
    - Queue max: 3x observed (min 10)
    """
    # Conservative tuning: aim for 20% improvement
    p95_target = max(min(int(observed_p95 * 0.8), 150), 40)
    queue_max = max(10, int(observed_queue * 3))
    
    return {
        "p95_target_ms": p95_target,
        "queue_max_depth": queue_max
    }

def log_tuning_change(param: str, old_val: str, new_val: str, note: str, actor: str = "auto_tune"):
    """Record tuning change to audit log"""
    conn = sqlite3.connect("levqor.db")
    ts = int(time.time())
    conn.execute(
        "INSERT INTO tuning_audit(ts, actor, param, old_val, new_val, note) VALUES(?,?,?,?,?,?)",
        [ts, actor, param, old_val, new_val, note]
    )
    conn.commit()
    conn.close()
    logger.info(f"Tuning audit: {param} {old_val} → {new_val}")

def suggest_tuning(current_p95: float = 80, current_queue: int = 1) -> Dict[str, Any]:
    """
    Generate tuning suggestions based on current metrics.
    
    Returns dry-run diff with suggested parameter changes.
    Safe to call - does not apply changes automatically.
    """
    try:
        # Fetch real metrics if available
        metrics = get_recent_metrics()
        obs_p95 = metrics.get("observed_p95", current_p95)
        obs_queue = metrics.get("queue_depth_p95", current_queue)
        
        # Compute new targets
        targets = compute_targets(obs_p95, obs_queue)
        
        # Calculate diff
        diff = {
            "p95_ms": {
                "current": int(current_p95),
                "suggested": targets["p95_target_ms"],
                "delta": targets["p95_target_ms"] - int(current_p95)
            },
            "queue_max": {
                "current": current_queue,
                "suggested": targets["queue_max_depth"],
                "delta": targets["queue_max_depth"] - current_queue
            }
        }
        
        return {
            "status": "ok",
            "dry_run": True,
            "observed_p95_ms": obs_p95,
            "observed_queue_depth": obs_queue,
            "suggestions": targets,
            "diff": diff,
            "note": "Review diff before applying. Use /api/admin/tuning/apply to activate."
        }
        
    except Exception as e:
        logger.error(f"Auto-tune error: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
