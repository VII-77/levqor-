CREATE INDEX IF NOT EXISTS ix_users_email          ON users(email);
CREATE INDEX IF NOT EXISTS ix_supp_hash            ON suppression(hash);
CREATE INDEX IF NOT EXISTS ix_conv_user_created    ON partner_conversions(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_conv_code_created    ON partner_conversions(partner_code, created_at DESC);
