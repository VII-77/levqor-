#!/bin/bash
set -e

timestamp=$(date -u +%Y%m%dT%H%M%SZ)
backup_file="backups/backup_${timestamp}.db"

mkdir -p backups
mkdir -p logs

if [ ! -f "levqor.db" ]; then
  echo "[ERROR] Database file levqor.db not found" | tee -a logs/backup.log
  exit 1
fi

cp levqor.db "$backup_file"

if [ -f "$backup_file" ]; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Backup successful: $backup_file" | tee -a logs/backup.log
  exit 0
else
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Backup failed: $backup_file" | tee -a logs/backup.log
  exit 1
fi
