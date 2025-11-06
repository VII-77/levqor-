# Levqor Database Migration Guide

## Overview
Levqor uses **SQLite by default** for simplicity and cost-effectiveness. PostgreSQL support is available as an optional upgrade path.

## Current Setup: SQLite
- **Database:** `data/levqor.db`
- **Mode:** WAL (Write-Ahead Logging)
- **Backups:** Daily automated backups to `backups/`
- **Cost:** $0
- **Scales to:** ~100K users easily

## When to Migrate to PostgreSQL
Consider PostgreSQL when:
- You exceed 100K users
- You need multi-region replication
- You require advanced analytics
- Your team needs concurrent write access

## Migration Steps

### Option 1: Supabase (Recommended)
1. Create Supabase project: https://supabase.com
2. Copy `DATABASE_URL` from settings
3. Run migration script:
```bash
# Export SQLite data
python3 db/migrations/export_sqlite.py > data/export.sql

# Import to Supabase
psql $DATABASE_URL < db/migrations/001_initial_schema.sql
psql $DATABASE_URL < data/export.sql
```

4. Switch database:
```bash
# Add to Replit Secrets
DB_TYPE=postgres
DATABASE_URL=postgresql://...
```

5. Restart application

### Option 2: Neon (Alternative)
1. Create Neon project: https://neon.tech
2. Follow same steps as Supabase
3. Use Neon's `DATABASE_URL`

### Option 3: Railway (Alternative)
1. Create Railway project: https://railway.app
2. Add PostgreSQL service
3. Copy connection string
4. Follow migration steps above

## Database Adapter

The application includes a **non-disruptive adapter** (`db/migrations/postgres_adapter.py`) that:
- Defaults to SQLite
- Switches to PostgreSQL when `DB_TYPE=postgres` is set
- Translates queries automatically
- Maintains backward compatibility

### Using the Adapter
```python
from db.migrations.postgres_adapter import DatabaseAdapter

db = DatabaseAdapter()
conn = db.connect()  # Uses SQLite or PostgreSQL based on env
cursor = db.execute("SELECT * FROM users WHERE email = ?", ("user@example.com",))
```

## Migration Checklist
- [ ] Backup current SQLite database
- [ ] Create PostgreSQL instance (Supabase/Neon/Railway)
- [ ] Run schema migration (`001_initial_schema.sql`)
- [ ] Export and import data
- [ ] Set environment variables
- [ ] Test application endpoints
- [ ] Monitor for errors
- [ ] Verify backup system works

## Rollback Plan
If migration fails:
1. Remove `DB_TYPE=postgres` env variable
2. Restart application
3. Application reverts to SQLite automatically

## Costs Comparison
| Database | Free Tier | Paid (Small) | Paid (Medium) |
|----------|-----------|--------------|---------------|
| SQLite | $0 | $0 | $0 |
| Supabase | 500MB free | $25/month (8GB) | $99/month (unlimited) |
| Neon | 0.5GB free | $19/month (10GB) | $69/month (50GB) |
| Railway | 512MB free | $5/month (1GB) | $20/month (10GB) |

## Recommendation
**Stick with SQLite** until you have:
- 50K+ active users
- Multi-region deployment needs
- Team requiring concurrent database access

SQLite is production-ready and used by:
- Cloudflare (D1)
- Fly.io (LiteFS)
- Expensify (100M+ users)

## Status: IMPLEMENTED (Non-Disruptive)
- ✅ PostgreSQL adapter created
- ✅ Migration scripts ready
- ✅ SQLite remains default
- ⏳ Migration requires user action (create Postgres instance)
