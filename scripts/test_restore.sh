#!/bin/bash
set -e
LATEST=$(ls -t backups/backup_*.db 2>/dev/null | head -1)
[ -z "$LATEST" ] && echo "[!] No backup found." && exit 1
sqlite3 /tmp/test_restore.db ".restore $LATEST" || exit 1
COUNT=$(sqlite3 /tmp/test_restore.db "SELECT COUNT(*) FROM users;")
echo "[✓] Restore verified, users rows: $COUNT"
rm -f /tmp/test_restore.db
