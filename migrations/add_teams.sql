-- Team/Organization system for Levqor

CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    owner_user_id TEXT NOT NULL,
    credits_pool INTEGER DEFAULT 0,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    meta TEXT
);

CREATE INDEX IF NOT EXISTS idx_orgs_owner ON organizations(owner_user_id);

CREATE TABLE IF NOT EXISTS team_members (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('owner', 'admin', 'member')),
    joined_at REAL NOT NULL,
    invited_by TEXT,
    UNIQUE(org_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_team_org ON team_members(org_id);
CREATE INDEX IF NOT EXISTS idx_team_user ON team_members(user_id);

CREATE TABLE IF NOT EXISTS team_invitations (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'member')),
    invited_by TEXT NOT NULL,
    created_at REAL NOT NULL,
    expires_at REAL NOT NULL,
    accepted BOOLEAN DEFAULT 0,
    UNIQUE(org_id, email)
);

CREATE INDEX IF NOT EXISTS idx_invites_org ON team_invitations(org_id);
CREATE INDEX IF NOT EXISTS idx_invites_email ON team_invitations(email);

-- Migrate existing users to have default personal organization
-- This runs only once during migration
