#!/bin/bash
set -e
LATEST=$(ls -t backups/backup_*.db 2>/dev/null | head -1)
[ -z "$LATEST" ] && echo "[!] No backup found." && exit 1

python3 << EOF
import sqlite3
import shutil

try:
    shutil.copy('$LATEST', '/tmp/test_restore.db')
    conn = sqlite3.connect('/tmp/test_restore.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    print(f'[✓] Restore verified, users rows: {count}')
    conn.close()
except Exception as e:
    print(f'[!] Restore failed: {e}')
    exit(1)
finally:
    import os
    if os.path.exists('/tmp/test_restore.db'):
        os.remove('/tmp/test_restore.db')
EOF
