"""
Adaptive pricing model based on usage, performance, and costs.
Server-side suggestion only - no auto-application unless flag enabled.
"""
import logging

logger = logging.getLogger("levqor.pricing")


def suggest_price(monthly_runs, p95_ms, openai_cost, infra_cost, refunds):
    """
    Calculate suggested pricing based on multiple factors.
    
    Args:
        monthly_runs: Number of job runs in last 30 days
        p95_ms: P95 latency in milliseconds
        openai_cost: OpenAI costs in last 30 days ($)
        infra_cost: Infrastructure costs in last 30 days ($)
        refunds: Refund amount in last 30 days ($)
    
    Returns:
        tuple: (target_price, rationale_dict)
    """
    base_price = 19.0
    
    # Load factor: increase price with volume (cap at 2x)
    load_factor = min(2.0, 0.5 + monthly_runs / 1000.0)
    
    # Performance bonus/penalty
    if p95_ms < 80:
        perf_bonus = -2.0  # Reward for excellent performance
    elif p95_ms < 150:
        perf_bonus = 0.0   # Neutral for acceptable performance
    else:
        perf_bonus = 2.0   # Penalty for poor performance
    
    # Cost floor: ensure profitability (1.3x cost recovery)
    runs_k = max(1, monthly_runs / 1000.0)
    total_costs = openai_cost + infra_cost + refunds
    cost_floor = (total_costs * 1.3) / runs_k
    
    # Calculate target price
    target = base_price * load_factor + perf_bonus
    target = max(target, max(9.0, cost_floor))  # Never below $9 or cost floor
    target = round(target, 2)
    
    rationale = {
        "base": base_price,
        "load_factor": round(load_factor, 2),
        "perf_bonus": perf_bonus,
        "cost_floor": round(cost_floor, 2),
        "monthly_runs": monthly_runs,
        "p95_ms": p95_ms
    }
    
    logger.info(f"Pricing suggestion: ${target} (rationale: {rationale})")
    
    return target, rationale
