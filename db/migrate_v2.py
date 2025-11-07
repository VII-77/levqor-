import sqlite3
import psycopg2
import os
import sys
from datetime import datetime

SQLITE_DB = os.getenv("SQLITE_DB_PATH", "data/levqor.db")
POSTGRES_URL = os.getenv("DATABASE_URL")

def get_sqlite_conn():
    return sqlite3.connect(SQLITE_DB)

def get_postgres_conn():
    return psycopg2.connect(POSTGRES_URL)

def create_postgres_schema(pg_conn):
    cursor = pg_conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            locale TEXT,
            currency TEXT,
            meta TEXT,
            credits_remaining INTEGER DEFAULT 50,
            created_at DOUBLE PRECISION,
            updated_at DOUBLE PRECISION,
            ref_code TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics(
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            payload TEXT,
            ref TEXT,
            timestamp DOUBLE PRECISION NOT NULL,
            created_at DOUBLE PRECISION
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_type ON metrics(type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals(
            id TEXT PRIMARY KEY,
            referrer_user_id TEXT NOT NULL,
            referee_email TEXT NOT NULL,
            referee_user_id TEXT,
            created_at DOUBLE PRECISION NOT NULL,
            credited INTEGER DEFAULT 0,
            utm_source TEXT,
            utm_medium TEXT,
            utm_campaign TEXT
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_referrals_referee_email ON referrals(referee_email)")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_daily(
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            day TEXT NOT NULL,
            jobs_run INTEGER DEFAULT 0,
            cost_saving DOUBLE PRECISION DEFAULT 0,
            created_at DOUBLE PRECISION NOT NULL,
            UNIQUE(user_id, day)
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_user_day ON usage_daily(user_id, day)")
    
    pg_conn.commit()
    print("✅ PostgreSQL schema created")

def migrate_table(sqlite_conn, pg_conn, table_name):
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = sqlite_cursor.fetchone()[0]
    
    if count == 0:
        print(f"  {table_name}: 0 rows (empty table)")
        return 0
    
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    columns = [desc[0] for desc in sqlite_cursor.description]
    
    placeholders = ','.join(['%s'] * len(columns))
    column_names = ','.join(columns)
    
    insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
    
    pg_cursor.executemany(insert_query, rows)
    pg_conn.commit()
    
    print(f"  {table_name}: {len(rows)} rows migrated")
    return len(rows)

def verify_parity(sqlite_conn, pg_conn):
    tables = ['users', 'metrics', 'referrals', 'usage_daily']
    parity_ok = True
    
    print("\n🔍 Parity Verification:")
    print("-" * 50)
    
    for table in tables:
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
        sqlite_count = sqlite_cursor.fetchone()[0]
        
        pg_cursor.execute(f"SELECT COUNT(*) FROM {table}")
        pg_count = pg_cursor.fetchone()[0]
        
        match = "✅" if sqlite_count == pg_count else "❌"
        print(f"{match} {table:15} | SQLite: {sqlite_count:6} | PostgreSQL: {pg_count:6}")
        
        if sqlite_count != pg_count:
            parity_ok = False
    
    print("-" * 50)
    return parity_ok

def main():
    print("=" * 60)
    print("Levqor SQLite → PostgreSQL Migration")
    print("=" * 60)
    print()
    
    if not os.path.exists(SQLITE_DB):
        print(f"✅ No existing SQLite database found at {SQLITE_DB}")
        print("✅ Creating fresh PostgreSQL schema...")
        pg_conn = get_postgres_conn()
        create_postgres_schema(pg_conn)
        pg_conn.close()
        print("\n✅ Migration Complete - Fresh installation")
        return
    
    print(f"📁 SQLite DB: {SQLITE_DB}")
    print(f"🐘 PostgreSQL: {POSTGRES_URL[:50]}...")
    print()
    
    try:
        sqlite_conn = get_sqlite_conn()
        pg_conn = get_postgres_conn()
        
        print("Step 1: Creating PostgreSQL schema...")
        create_postgres_schema(pg_conn)
        
        print("\nStep 2: Migrating data...")
        tables = ['users', 'referrals', 'metrics', 'usage_daily']
        total_migrated = 0
        
        for table in tables:
            try:
                count = migrate_table(sqlite_conn, pg_conn, table)
                total_migrated += count
            except Exception as e:
                print(f"  ⚠️  {table}: {e}")
        
        print(f"\n✅ Total rows migrated: {total_migrated}")
        
        print("\nStep 3: Verifying parity...")
        parity_ok = verify_parity(sqlite_conn, pg_conn)
        
        if parity_ok:
            print("\n✅ PARITY CHECK PASS - All counts match!")
        else:
            print("\n❌ PARITY CHECK FAIL - Counts mismatch!")
            sys.exit(1)
        
        sqlite_conn.close()
        pg_conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Migration Complete Successfully")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ FAILING STEP: Migration failed")
        print(f"Reason: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
