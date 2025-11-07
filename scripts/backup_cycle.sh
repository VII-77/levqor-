#!/bin/bash
set -e

# Backup Cycle with Checksum Verification & Off-site Upload
# Creates SQLite backup, generates checksum, and optionally uploads to Google Drive

STAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
BACKUP_FILE="$BACKUP_DIR/db_$STAMP.sqlite"
CHECKSUM_FILE="$BACKUP_DIR/checksums.txt"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

echo "[📦] Starting backup cycle: $STAMP"

# Create backup
if [ -f "levqor.db" ]; then
    sqlite3 levqor.db ".backup $BACKUP_FILE"
    echo "[✓] Database backup created: $BACKUP_FILE"
else
    echo "[!] levqor.db not found - skipping backup"
    exit 1
fi

# Generate and store checksum
sha256sum "$BACKUP_FILE" | tee -a "$CHECKSUM_FILE"
echo "[✓] Checksum recorded in $CHECKSUM_FILE"

# Get backup size
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "[ℹ] Backup size: $BACKUP_SIZE"

# Upload to Google Drive if configured
if [ -n "$GDRIVE_FOLDER_ID" ]; then
    if command -v gdrive &> /dev/null; then
        echo "[📤] Uploading to Google Drive..."
        gdrive upload --parent "$GDRIVE_FOLDER_ID" "$BACKUP_FILE" --name "levqor_db_$STAMP.sqlite"
        echo "[✓] Uploaded to Google Drive"
    else
        echo "[!] gdrive CLI not found - install from: https://github.com/glotlabs/gdrive"
        echo "[ℹ] Skipping off-site upload"
    fi
else
    echo "[ℹ] GDRIVE_FOLDER_ID not set - skipping off-site upload"
fi

# Cleanup old backups (keep last 30)
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/db_*.sqlite 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 30 ]; then
    echo "[🗑️] Cleaning up old backups (keeping last 30)..."
    ls -1t "$BACKUP_DIR"/db_*.sqlite | tail -n +31 | xargs rm -f
    echo "[✓] Cleanup complete"
fi

echo "[✓] Backup cycle complete: $STAMP"
echo ""
echo "Latest backups:"
ls -lht "$BACKUP_DIR"/db_*.sqlite | head -5 | awk '{print "  ", $9, "("$5")"}'
