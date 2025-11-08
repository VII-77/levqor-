"""
SLO Watchdog - Monitors SLO compliance and triggers auto-recovery
"""
import logging
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, Any

log = logging.getLogger("levqor.slo_watchdog")

class SLOWatchdog:
    def __init__(self):
        self.breach_history = deque(maxlen=10)
        self.last_recovery_trigger = None
        self.cooldown_minutes = 30
        
    def check_slo(
        self,
        p99_latency_ms: float = 0,
        error_rate: float = 0,
        availability: float = 1.0
    ) -> Dict[str, Any]:
        """
        Check SLO compliance
        
        Thresholds:
        - P99 latency < 200ms
        - Error rate < 0.5%
        - Availability > 99.9%
        """
        now = datetime.utcnow()
        breaches = []
        
        if p99_latency_ms > 200:
            breaches.append(f"P99 latency {p99_latency_ms}ms > 200ms")
        
        if error_rate > 0.005:
            breaches.append(f"Error rate {error_rate:.2%} > 0.5%")
        
        if availability < 0.999:
            breaches.append(f"Availability {availability:.2%} < 99.9%")
        
        breach_detected = len(breaches) > 0
        
        self.breach_history.append({
            "timestamp": now.isoformat(),
            "breaches": breaches,
            "breach_detected": breach_detected
        })
        
        should_trigger_recovery = False
        recent_breaches = [
            b for b in list(self.breach_history)
            if b["breach_detected"]
            and datetime.fromisoformat(b["timestamp"]) > now - timedelta(minutes=10)
        ]
        
        if len(recent_breaches) >= 3:
            if self.last_recovery_trigger is None:
                should_trigger_recovery = True
            else:
                time_since_last = (now - self.last_recovery_trigger).total_seconds() / 60
                if time_since_last > self.cooldown_minutes:
                    should_trigger_recovery = True
        
        if should_trigger_recovery:
            self.last_recovery_trigger = now
            log.warning(f"SLO breach threshold exceeded, triggering recovery. Breaches: {breaches}")
        
        return {
            "slo_compliant": not breach_detected,
            "breaches": breaches,
            "recent_breach_count": len(recent_breaches),
            "should_trigger_recovery": should_trigger_recovery,
            "next_check_allowed": (
                (self.last_recovery_trigger + timedelta(minutes=self.cooldown_minutes)).isoformat()
                if self.last_recovery_trigger else now.isoformat()
            )
        }


_watchdog = None

def get_watchdog() -> SLOWatchdog:
    """Singleton watchdog instance"""
    global _watchdog
    if _watchdog is None:
        _watchdog = SLOWatchdog()
    return _watchdog
