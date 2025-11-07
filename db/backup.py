"""
PostgreSQL Backup System
Daily automated backups with 7-day retention
"""
import os
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

BACKUP_DIR = Path("db/backups/pg")
BACKUP_RETENTION_DAYS = 7

# PostgreSQL connection from env
PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")


def create_backup() -> dict:
    """Create PostgreSQL backup using pg_dump"""
    try:
        # Ensure backup directory exists
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        backup_file = BACKUP_DIR / f"backup_{timestamp}.sql"
        
        # Build pg_dump command
        env = os.environ.copy()
        env["PGPASSWORD"] = PGPASSWORD
        
        cmd = [
            "pg_dump",
            "-h", PGHOST,
            "-p", PGPORT,
            "-U", PGUSER,
            "-d", PGDATABASE,
            "-F", "p",  # Plain SQL format
            "-f", str(backup_file),
            "--no-owner",
            "--no-acl"
        ]
        
        # Execute backup
        logger.info(f"Starting PostgreSQL backup to {backup_file}")
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            logger.error(f"Backup failed: {result.stderr}")
            return {
                "success": False,
                "error": result.stderr,
                "timestamp": timestamp
            }
        
        # Get backup file size
        file_size = backup_file.stat().st_size
        
        logger.info(f"Backup completed successfully: {backup_file} ({file_size} bytes)")
        
        # Clean old backups
        cleanup_old_backups()
        
        return {
            "success": True,
            "file": str(backup_file),
            "size_bytes": file_size,
            "timestamp": timestamp
        }
    
    except Exception as e:
        logger.error(f"Backup error: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


def cleanup_old_backups():
    """Remove backups older than retention period"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=BACKUP_RETENTION_DAYS)
        deleted = 0
        
        for backup_file in BACKUP_DIR.glob("backup_*.sql"):
            # Extract timestamp from filename
            try:
                timestamp_str = backup_file.stem.split("_")[1]
                file_date = datetime.strptime(timestamp_str, "%Y%m%dT%H%M%SZ")
                
                if file_date < cutoff_date:
                    backup_file.unlink()
                    deleted += 1
                    logger.info(f"Deleted old backup: {backup_file}")
            
            except Exception as e:
                logger.warning(f"Could not parse backup file {backup_file}: {e}")
        
        if deleted > 0:
            logger.info(f"Cleaned up {deleted} old backups")
    
    except Exception as e:
        logger.error(f"Backup cleanup error: {e}")


def get_backup_status() -> dict:
    """Get backup status and list recent backups"""
    try:
        backups = sorted(BACKUP_DIR.glob("backup_*.sql"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        backup_list = []
        total_size = 0
        
        for backup_file in backups[:10]:  # Last 10 backups
            stat = backup_file.stat()
            backup_list.append({
                "file": backup_file.name,
                "size_bytes": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
            total_size += stat.st_size
        
        return {
            "backup_count": len(backups),
            "recent_backups": backup_list,
            "total_size_bytes": total_size,
            "retention_days": BACKUP_RETENTION_DAYS
        }
    
    except Exception as e:
        logger.error(f"Backup status error: {e}")
        return {
            "error": str(e),
            "backup_count": 0,
            "recent_backups": [],
            "total_size_bytes": 0
        }


if __name__ == "__main__":
    # Manual backup execution
    result = create_backup()
    print(f"Backup result: {result}")
