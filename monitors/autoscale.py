"""
Autoscale Controller - SLO-based worker scaling with cost guardrails
"""
import os
import json
import logging
import sqlite3
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, Any, Literal

log = logging.getLogger("levqor.autoscale")

ACTION = Literal["scale_up", "scale_down", "freeze", "hold"]

class AutoscaleController:
    def __init__(self):
        self.daily_spend_limit = float(os.environ.get("DAILY_SPEND_LIMIT", 50))
        self.config_path = "config/flags.json"
        self.metrics_history = deque(maxlen=10)
        self.last_scale_down_check = datetime.utcnow()
        self.scale_events = 0
    
    def _get_flag(self, key: str, default: str = "false") -> bool:
        """Read feature flag from database"""
        try:
            conn = sqlite3.connect("levqor.db")
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM feature_flags WHERE key=?", (key,))
            row = cursor.fetchone()
            conn.close()
            value = row[0] if row else default
            return value.lower() == "true"
        except Exception:
            return default.lower() == "true"
        
    def get_current_worker_count(self) -> int:
        """Read current worker count from config"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    return config.get("WORKER_COUNT", 2)
        except Exception as e:
            log.warning(f"Failed to read worker count: {e}")
        return 2
    
    def set_worker_count(self, count: int) -> bool:
        """Update worker count in config"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            config = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
            
            config["WORKER_COUNT"] = count
            config["LAST_AUTOSCALE"] = datetime.utcnow().isoformat()
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            log.info(f"Updated worker count to {count}")
            self.scale_events += 1
            return True
        except Exception as e:
            log.error(f"Failed to set worker count: {e}")
            return False
    
    def _get_profit_margin(self) -> float:
        """
        Get current profit margin from KV store.
        Returns margin percentage (0-100).
        """
        try:
            conn = sqlite3.connect("levqor.db")
            c = conn.cursor()
            
            # Get revenue and costs from KV
            c.execute("SELECT value FROM kv WHERE key='stripe_revenue_30d'")
            revenue_row = c.fetchone()
            revenue = float(revenue_row[0]) if revenue_row else 0.0
            
            c.execute("SELECT value FROM kv WHERE key='openai_cost_30d'")
            openai_row = c.fetchone()
            openai_cost = float(openai_row[0]) if openai_row else 0.0
            
            c.execute("SELECT value FROM kv WHERE key='infra_cost_30d'")
            infra_row = c.fetchone()
            infra_cost = float(infra_row[0]) if infra_row else 0.0
            
            conn.close()
            
            total_cost = openai_cost + infra_cost
            if revenue == 0:
                return 0.0
            
            margin = ((revenue - total_cost) / revenue) * 100
            return round(margin, 2)
            
        except Exception as e:
            log.warning(f"Failed to calculate profit margin: {e}")
            return 100.0  # Default to allowing scale if we can't check
    
    def get_spend_last_24h(self) -> float:
        """Estimate spend from last 24h (placeholder - integrate with billing)"""
        try:
            import sqlite3
            db_path = os.environ.get("SQLITE_PATH", "levqor.db")
            if not os.path.exists(db_path):
                return 0.0
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cutoff = (datetime.utcnow() - timedelta(hours=24)).isoformat()
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE created_at > ?",
                (cutoff,)
            )
            new_users = cursor.fetchone()[0]
            conn.close()
            
            return new_users * 0.1
        except Exception as e:
            log.warning(f"Failed to calculate spend: {e}")
            return 0.0
    
    def decide_action(
        self,
        queue_depth: int = 0,
        p95_latency_ms: float = 0,
        error_rate: float = 0,
        spend_last_24h: float = None
    ) -> Dict[str, Any]:
        """
        Decide scaling action based on SLO metrics
        
        Policy:
        - If P95>150ms OR queue_depth>10 → scale_up (max 4 workers)
        - If P95<40ms AND queue_depth==0 for 10min → scale_down (min 1)
        - If spend >= 90% of daily limit → freeze scale_up
        - If STABILIZE_MODE=true → freeze all scaling
        """
        # Check STABILIZE_MODE first
        if self._get_flag("STABILIZE_MODE", "false"):
            return {
                "action": "hold",
                "current_workers": self.get_current_worker_count(),
                "target_workers": self.get_current_worker_count(),
                "reason": "STABILIZE_MODE enabled - all scaling frozen",
                "timestamp": datetime.utcnow().isoformat(),
                "stabilize_mode": True
            }
        
        # Check if autoscaling is enabled
        if not self._get_flag("AUTOSCALE_ENABLED", "false"):
            return {
                "action": "hold",
                "current_workers": self.get_current_worker_count(),
                "target_workers": self.get_current_worker_count(),
                "reason": "Autoscaling disabled via feature flag",
                "timestamp": datetime.utcnow().isoformat(),
                "autoscale_enabled": False
            }
        
        # Profit guard: check if we're profitable before allowing scale-up
        profit_margin = self._get_profit_margin()
        profit_frozen = profit_margin < 10.0  # Require at least 10% margin
        
        current_workers = self.get_current_worker_count()
        
        if spend_last_24h is None:
            spend_last_24h = self.get_spend_last_24h()
        
        spend_threshold = self.daily_spend_limit * 0.9
        spend_frozen = spend_last_24h >= spend_threshold
        
        self.metrics_history.append({
            "ts": datetime.utcnow().isoformat(),
            "queue_depth": queue_depth,
            "p95_latency_ms": p95_latency_ms
        })
        
        action: ACTION = "hold"
        reason = "All metrics within acceptable range"
        target_workers = current_workers
        
        if p95_latency_ms > 150 or queue_depth > 10:
            if spend_frozen:
                action = "freeze"
                reason = f"Would scale up but spend ({spend_last_24h:.2f}) >= 90% limit ({spend_threshold:.2f})"
            elif profit_frozen:
                action = "freeze"
                reason = f"Would scale up but profit margin ({profit_margin:.1f}%) < 10% threshold"
            elif current_workers < 4:
                action = "scale_up"
                target_workers = current_workers + 1
                reason = f"P95={p95_latency_ms}ms or queue_depth={queue_depth} exceeds threshold"
            else:
                action = "hold"
                reason = "Already at max workers (4)"
        
        elif p95_latency_ms < 40 and queue_depth == 0:
            recent_idle = all(
                m.get("queue_depth", 0) == 0
                for m in list(self.metrics_history)[-2:]
            )
            
            if recent_idle and current_workers > 1:
                action = "scale_down"
                target_workers = current_workers - 1
                reason = "Low latency and idle queue for extended period"
        
        return {
            "action": action,
            "current_workers": current_workers,
            "target_workers": target_workers,
            "reason": reason,
            "metrics": {
                "queue_depth": queue_depth,
                "p95_latency_ms": p95_latency_ms,
                "error_rate": error_rate,
                "spend_last_24h": spend_last_24h,
                "spend_limit": self.daily_spend_limit,
                "spend_frozen": spend_frozen,
                "profit_margin_pct": profit_margin,
                "profit_frozen": profit_frozen
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def apply_action(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Apply the scaling decision"""
        action = decision["action"]
        
        if action in ("hold", "freeze"):
            return {
                "ok": True,
                "applied": False,
                "action": action,
                "message": decision["reason"]
            }
        
        target = decision["target_workers"]
        success = self.set_worker_count(target)
        
        return {
            "ok": success,
            "applied": success,
            "action": action,
            "workers": target,
            "message": f"Worker count updated to {target}" if success else "Failed to update worker count"
        }
    
    def get_prometheus_metrics(self) -> Dict[str, float]:
        """Export Prometheus-compatible metrics"""
        return {
            "levqor_worker_target": self.get_current_worker_count(),
            "levqor_autoscale_events_total": self.scale_events
        }


_controller = None

def get_controller() -> AutoscaleController:
    """Singleton controller instance"""
    global _controller
    if _controller is None:
        _controller = AutoscaleController()
    return _controller
