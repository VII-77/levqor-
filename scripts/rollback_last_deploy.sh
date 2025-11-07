#!/bin/bash
set -e
PREV=$(git log --pretty=format:%h -2 | tail -1)
echo "[Rollback] Reverting to commit $PREV..."
echo "[!] WARNING: This will force push to main branch!"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read
git checkout $PREV
git push --force origin main
echo "[✓] Rolled back to $PREV"
