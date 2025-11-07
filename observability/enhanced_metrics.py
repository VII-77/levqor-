"""
Enhanced Prometheus Metrics
Adds P95 latency, queue depth, error rates, connector metrics
"""
import time
import logging
from collections import defaultdict
from typing import Dict, List

logger = logging.getLogger(__name__)

# Metrics storage
_latency_samples: Dict[str, List[float]] = defaultdict(list)
_error_counts: Dict[str, int] = defaultdict(int)
_connector_errors: Dict[str, int] = defaultdict(int)
_ai_costs = {"total_usd": 0.0, "daily_usd": 0.0, "last_reset": time.time()}


def record_latency(endpoint: str, duration_ms: float):
    """Record API latency for endpoint"""
    _latency_samples[endpoint].append(duration_ms)
    
    # Keep only last 1000 samples per endpoint
    if len(_latency_samples[endpoint]) > 1000:
        _latency_samples[endpoint] = _latency_samples[endpoint][-1000:]


def record_error(error_type: str):
    """Record error occurrence"""
    _error_counts[error_type] += 1


def record_connector_error(provider: str, status_code: int):
    """Record connector 5xx error"""
    if 500 <= status_code < 600:
        _connector_errors[provider] += 1


def record_ai_cost(cost_usd: float):
    """Record AI API cost"""
    _ai_costs["total_usd"] += cost_usd
    _ai_costs["daily_usd"] += cost_usd


def calculate_p95(samples: List[float]) -> float:
    """Calculate 95th percentile"""
    if not samples:
        return 0.0
    
    sorted_samples = sorted(samples)
    index = int(len(sorted_samples) * 0.95)
    return sorted_samples[index] if index < len(sorted_samples) else sorted_samples[-1]


def get_enhanced_metrics() -> str:
    """Generate Prometheus metrics text format"""
    lines = []
    
    # API Latency P95
    lines.append("# HELP api_latency_p95_ms 95th percentile API latency in milliseconds")
    lines.append("# TYPE api_latency_p95_ms gauge")
    for endpoint, samples in _latency_samples.items():
        if samples:
            p95 = calculate_p95(samples)
            lines.append(f'api_latency_p95_ms{{endpoint="{endpoint}"}} {p95:.2f}')
    
    # Queue depth (from queue.worker)
    try:
        from queue.worker import get_queue_health
        health = get_queue_health()
        
        lines.append("# HELP queue_depth Number of jobs in queue")
        lines.append("# TYPE queue_depth gauge")
        lines.append(f"queue_depth {health.get('depth', 0)}")
        
        lines.append("# HELP dlq_depth Number of jobs in dead letter queue")
        lines.append("# TYPE dlq_depth gauge")
        lines.append(f"dlq_depth {health.get('dlq', 0)}")
    except:
        pass
    
    # Error rate
    lines.append("# HELP error_rate_total Total errors by type")
    lines.append("# TYPE error_rate_total counter")
    for error_type, count in _error_counts.items():
        lines.append(f'error_rate_total{{type="{error_type}"}} {count}')
    
    # Connector 5xx errors
    lines.append("# HELP connector_5xx_total Total 5xx errors by provider")
    lines.append("# TYPE connector_5xx_total counter")
    for provider, count in _connector_errors.items():
        lines.append(f'connector_5xx_total{{provider="{provider}"}} {count}')
    
    # AI costs
    lines.append("# HELP ai_cost_daily_usd Daily AI API cost in USD")
    lines.append("# TYPE ai_cost_daily_usd gauge")
    lines.append(f"ai_cost_daily_usd {_ai_costs['daily_usd']:.4f}")
    
    # Rate limit hits
    try:
        from middleware.ratelimit import get_rate_limit_metrics
        rl_metrics = get_rate_limit_metrics()
        
        lines.append("# HELP rate_limit_hits_total Total rate limit hits by scope")
        lines.append("# TYPE rate_limit_hits_total counter")
        for scope, count in rl_metrics.items():
            lines.append(f'rate_limit_hits_total{{scope="{scope}"}} {count}')
    except:
        pass
    
    # Abuse blocks
    try:
        from abuse.controls import get_abuse_metrics
        abuse_metrics = get_abuse_metrics()
        
        for metric, value in abuse_metrics.items():
            lines.append(f"# HELP {metric} Abuse control blocks")
            lines.append(f"# TYPE {metric} counter")
            lines.append(f"{metric} {value}")
    except:
        pass
    
    return "\n".join(lines)


def reset_daily_metrics():
    """Reset daily metrics (called by scheduler)"""
    current_time = time.time()
    if current_time - _ai_costs["last_reset"] >= 86400:  # 24 hours
        _ai_costs["daily_usd"] = 0.0
        _ai_costs["last_reset"] = current_time
        logger.info("Daily metrics reset")
