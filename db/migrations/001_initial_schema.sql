-- Levqor PostgreSQL Migration Script
-- Run this to migrate from SQLite to PostgreSQL

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    locale VARCHAR(10),
    currency VARCHAR(3) DEFAULT 'USD',
    credits_remaining INTEGER DEFAULT 50,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    ref_code VARCHAR(255),
    meta TEXT
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_ref_code ON users(ref_code);

-- Referrals table
CREATE TABLE IF NOT EXISTS referrals (
    id VARCHAR(255) PRIMARY KEY,
    referrer_user_id VARCHAR(255) NOT NULL,
    referee_email VARCHAR(255) NOT NULL,
    created_at REAL NOT NULL,
    credited INTEGER DEFAULT 0,
    utm_source VARCHAR(255),
    utm_medium VARCHAR(255),
    utm_campaign VARCHAR(255)
);

CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_user_id);
CREATE INDEX IF NOT EXISTS idx_referrals_referee ON referrals(referee_email);

-- Usage daily table
CREATE TABLE IF NOT EXISTS usage_daily (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    day VARCHAR(10) NOT NULL,
    jobs_run INTEGER DEFAULT 0,
    cost_saving REAL DEFAULT 0,
    UNIQUE(user_id, day)
);

CREATE INDEX IF NOT EXISTS idx_usage_user ON usage_daily(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_day ON usage_daily(day);

-- Organizations table
CREATE TABLE IF NOT EXISTS organizations (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_user_id VARCHAR(255) NOT NULL,
    credits_pool INTEGER DEFAULT 0,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    meta TEXT
);

CREATE INDEX IF NOT EXISTS idx_orgs_owner ON organizations(owner_user_id);

-- Team members table
CREATE TABLE IF NOT EXISTS team_members (
    id VARCHAR(255) PRIMARY KEY,
    org_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK(role IN ('owner', 'admin', 'member')),
    joined_at REAL NOT NULL,
    invited_by VARCHAR(255),
    UNIQUE(org_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_team_org ON team_members(org_id);
CREATE INDEX IF NOT EXISTS idx_team_user ON team_members(user_id);

-- Team invitations table
CREATE TABLE IF NOT EXISTS team_invitations (
    id VARCHAR(255) PRIMARY KEY,
    org_id VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK(role IN ('admin', 'member')),
    invited_by VARCHAR(255) NOT NULL,
    created_at REAL NOT NULL,
    expires_at REAL NOT NULL,
    accepted BOOLEAN DEFAULT FALSE,
    UNIQUE(org_id, email)
);

CREATE INDEX IF NOT EXISTS idx_invites_org ON team_invitations(org_id);
CREATE INDEX IF NOT EXISTS idx_invites_email ON team_invitations(email);
