"""
Partner/Affiliate Schema Upgrade for Phase-5
Adds commission tracking, revenue attribution, and payout management
"""

PARTNER_TABLES_SQL = """
-- Partners table (upgraded from simple referrals)
CREATE TABLE IF NOT EXISTS partners (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    partner_code TEXT UNIQUE NOT NULL,
    commission_rate REAL DEFAULT 0.20,
    status TEXT DEFAULT 'active',
    total_referrals INTEGER DEFAULT 0,
    total_revenue REAL DEFAULT 0.0,
    total_commission REAL DEFAULT 0.0,
    paid_commission REAL DEFAULT 0.0,
    pending_commission REAL DEFAULT 0.0,
    stripe_account_id TEXT,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Partner conversions (tracks revenue-generating events)
CREATE TABLE IF NOT EXISTS partner_conversions (
    id TEXT PRIMARY KEY,
    partner_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    conversion_type TEXT NOT NULL,
    revenue_amount REAL NOT NULL,
    commission_amount REAL NOT NULL,
    commission_rate REAL NOT NULL,
    stripe_payment_id TEXT,
    status TEXT DEFAULT 'pending',
    created_at REAL NOT NULL,
    paid_at REAL,
    FOREIGN KEY (partner_id) REFERENCES partners(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Partner payouts (tracks commission payments)
CREATE TABLE IF NOT EXISTS partner_payouts (
    id TEXT PRIMARY KEY,
    partner_id TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    stripe_transfer_id TEXT,
    created_at REAL NOT NULL,
    processed_at REAL,
    notes TEXT,
    FOREIGN KEY (partner_id) REFERENCES partners(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_partners_user_id ON partners(user_id);
CREATE INDEX IF NOT EXISTS idx_partners_code ON partners(partner_code);
CREATE INDEX IF NOT EXISTS idx_conversions_partner ON partner_conversions(partner_id);
CREATE INDEX IF NOT EXISTS idx_conversions_user ON partner_conversions(user_id);
CREATE INDEX IF NOT EXISTS idx_conversions_created ON partner_conversions(created_at);
CREATE INDEX IF NOT EXISTS idx_payouts_partner ON partner_payouts(partner_id);
CREATE INDEX IF NOT EXISTS idx_payouts_status ON partner_payouts(status);
"""

def upgrade_database(db_connection):
    """Execute schema upgrade for partner system"""
    cursor = db_connection.cursor()
    
    for statement in PARTNER_TABLES_SQL.split(';'):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)
    
    db_connection.commit()
    return True
