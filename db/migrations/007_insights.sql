-- v6.5 AI Insights & Smart Ops Schema
CREATE TABLE IF NOT EXISTS incidents(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  type TEXT,
  severity TEXT,
  payload_json TEXT,
  resolved_bool BOOLEAN DEFAULT 0,
  resolution_note TEXT
);

CREATE TABLE IF NOT EXISTS postmortems(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  incident_id INTEGER,
  author TEXT,
  md TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (incident_id) REFERENCES incidents(id)
);

CREATE TABLE IF NOT EXISTS ai_cache(
  key TEXT PRIMARY KEY,
  value TEXT,
  expires_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feature_flags(
  key TEXT PRIMARY KEY,
  value TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed feature flags for v6.5
INSERT OR IGNORE INTO feature_flags(key, value) VALUES
  ('AI_INSIGHTS_ENABLED', 'false'),
  ('SMART_OPS_ENABLED', 'false'),
  ('WEEKLY_BRIEF_ENABLED', 'true'),
  ('AUTO_POSTMORTEM_ENABLED', 'false');
