#!/bin/bash
set -e

# Off-site backup upload to Google Drive
# Requires gdrive CLI: https://github.com/glotlabs/gdrive

BACKUP=$(ls -t backups/backup_*.db 2>/dev/null | head -1)

if [ -z "$BACKUP" ]; then
    echo "[!] No backup found in backups/ directory"
    exit 1
fi

DEST=$(date +%F)_$(basename $BACKUP)

if [ -z "$GDRIVE_FOLDER_ID" ]; then
    echo "[!] GDRIVE_FOLDER_ID not set - cannot upload"
    echo "    Set this environment variable to your Google Drive folder ID"
    exit 1
fi

if ! command -v gdrive &> /dev/null; then
    echo "[!] gdrive CLI not installed"
    echo "    Install from: https://github.com/glotlabs/gdrive"
    echo "    Or use alternative: rclone, aws s3 cp, etc."
    exit 1
fi

echo "[📤] Uploading $BACKUP to Google Drive..."
gdrive upload --parent "$GDRIVE_FOLDER_ID" "$BACKUP" --name "$DEST"
echo "[✓] Uploaded $DEST to Google Drive"
