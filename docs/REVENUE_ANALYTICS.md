# Revenue Analytics & KPI Tracking

## Overview
Track key revenue metrics: MRR, churn, ARPU, LTV.

## Internal KPI Dashboard

### Metrics Tracked
1. **MRR (Monthly Recurring Revenue)**
   - Credit pack purchases
   - Subscription equivalent
   - Growth rate

2. **Churn**
   - User churn (inactive >30 days)
   - Revenue churn (downgrades)
   - Cohort retention

3. **ARPU (Average Revenue Per User)**
   - Total revenue / active users
   - Segmented by cohort
   - Trend over time

4. **LTV (Lifetime Value)**
   - Average spend per user
   - By acquisition channel
   - Payback period

### Implementation

**Nightly Export Job:**
```python
# kpis/export.py
import json
from datetime import datetime, timedelta

def calculate_mrr():
    """Calculate Monthly Recurring Revenue"""
    db = get_db()
    last_30_days = time() - (30 * 86400)
    
    revenue = db.execute("""
        SELECT SUM(amount) FROM payments
        WHERE created_at >= ? AND status = 'succeeded'
    """, (last_30_days,)).fetchone()[0] or 0
    
    return revenue

def calculate_churn():
    """Calculate user churn rate"""
    db = get_db()
    thirty_days_ago = time() - (30 * 86400)
    sixty_days_ago = time() - (60 * 86400)
    
    active_30 = db.execute("""
        SELECT COUNT(DISTINCT user_id) FROM usage_daily
        WHERE day >= ?
    """, (datetime.fromtimestamp(thirty_days_ago).strftime('%Y-%m-%d'),)).fetchone()[0]
    
    active_60 = db.execute("""
        SELECT COUNT(DISTINCT user_id) FROM usage_daily
        WHERE day >= ?
    """, (datetime.fromtimestamp(sixty_days_ago).strftime('%Y-%m-%d'),)).fetchone()[0]
    
    churn = (active_60 - active_30) / active_60 if active_60 > 0 else 0
    return churn * 100

# Export to JSON
kpis = {
    "date": datetime.now().isoformat(),
    "mrr": calculate_mrr(),
    "churn_rate": calculate_churn(),
    "arpu": calculate_mrr() / get_active_users(),
    "total_users": get_total_users()
}

with open(f"data/kpis/{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
    json.dump(kpis, f, indent=2)
```

## ChartMogul Integration (Optional)

### Setup
1. Create ChartMogul account
2. Install SDK: `pip install chartmogul`
3. Add API key to secrets: `CHARTMOGUL_API_KEY`

### Send Data
```python
import chartmogul

chartmogul.Config.api_key = os.environ.get("CHARTMOGUL_API_KEY")

# Send subscription event
chartmogul.Subscription.create(
    customer_uuid="...",
    plan_uuid="...",
    data_source_uuid="...",
    cancellation_dates=[]
)
```

### Metrics Available
- MRR movements
- Churn analysis
- Cohort retention
- Revenue forecasting
- Custom segments

## Dashboard Access

### Internal Dashboard
```
GET /admin/revenue
```

Shows:
- Daily MRR chart
- Churn trend
- ARPU by cohort
- Top customers

### Export API
```
GET /api/v1/kpis/export?start=YYYY-MM-DD&end=YYYY-MM-DD
```

Returns JSON with all KPIs for date range.

## Costs
- **Internal:** $0 (built-in)
- **ChartMogul Starter:** $100/month
- **ChartMogul Pro:** $200/month

## Recommendation
Start with internal KPIs. Add ChartMogul when:
- Raising funds (investors love it)
- >$10K MRR
- Need advanced cohort analysis

## Status
- ✅ KPI calculation logic documented
- ✅ Export script template ready
- ⏳ ChartMogul requires API key (optional)
