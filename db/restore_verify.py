"""
Backup Restore Verification
Tests restore process and verifies data parity
Target: RTO ≤ 30 minutes
"""
import os
import subprocess
import logging
from datetime import datetime
from pathlib import Path
import psycopg2

logger = logging.getLogger(__name__)

BACKUP_DIR = Path("db/backups/pg")

# PostgreSQL connection
PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")


def get_table_counts(db_name: str) -> dict:
    """Get row counts for all tables in database"""
    try:
        conn = psycopg2.connect(
            host=PGHOST,
            port=PGPORT,
            database=db_name,
            user=PGUSER,
            password=PGPASSWORD
        )
        cursor = conn.cursor()
        
        # Get all user tables
        cursor.execute("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        # Count rows in each table
        counts = {}
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            counts[table] = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return counts
    
    except Exception as e:
        logger.error(f"Failed to get table counts: {e}")
        return {}


def restore_to_temp_db(backup_file: Path) -> dict:
    """
    Restore backup to temporary database and verify parity
    Returns parity percentage and timing info
    """
    start_time = datetime.utcnow()
    temp_db_name = f"levqor_restore_test_{int(start_time.timestamp())}"
    
    try:
        # Step 1: Get counts from production database
        logger.info("Getting counts from production database...")
        prod_counts = get_table_counts(PGDATABASE)
        
        if not prod_counts:
            return {
                "success": False,
                "error": "Failed to get production table counts"
            }
        
        # Step 2: Create temporary database
        logger.info(f"Creating temporary database: {temp_db_name}")
        conn = psycopg2.connect(
            host=PGHOST,
            port=PGPORT,
            database="postgres",  # Connect to postgres db to create new db
            user=PGUSER,
            password=PGPASSWORD
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {temp_db_name}")
        cursor.close()
        conn.close()
        
        # Step 3: Restore backup to temp database
        logger.info(f"Restoring backup {backup_file} to {temp_db_name}...")
        env = os.environ.copy()
        env["PGPASSWORD"] = PGPASSWORD
        
        cmd = [
            "psql",
            "-h", PGHOST,
            "-p", PGPORT,
            "-U", PGUSER,
            "-d", temp_db_name,
            "-f", str(backup_file),
            "-q"  # Quiet mode
        ]
        
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout
        )
        
        if result.returncode != 0:
            logger.error(f"Restore failed: {result.stderr}")
            return {
                "success": False,
                "error": f"Restore failed: {result.stderr}"
            }
        
        # Step 4: Get counts from restored database
        logger.info("Getting counts from restored database...")
        restore_counts = get_table_counts(temp_db_name)
        
        # Step 5: Calculate parity
        parity_results = {}
        total_tables = len(prod_counts)
        matching_tables = 0
        
        for table, prod_count in prod_counts.items():
            restore_count = restore_counts.get(table, 0)
            match = prod_count == restore_count
            if match:
                matching_tables += 1
            
            parity_results[table] = {
                "production": prod_count,
                "restored": restore_count,
                "match": match
            }
        
        parity_percentage = (matching_tables / total_tables * 100) if total_tables > 0 else 0
        
        # Step 6: Cleanup temp database
        logger.info(f"Cleaning up temporary database: {temp_db_name}")
        conn = psycopg2.connect(
            host=PGHOST,
            port=PGPORT,
            database="postgres",
            user=PGUSER,
            password=PGPASSWORD
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE {temp_db_name}")
        cursor.close()
        conn.close()
        
        # Calculate RTO
        end_time = datetime.utcnow()
        rto_seconds = (end_time - start_time).total_seconds()
        rto_minutes = rto_seconds / 60
        
        logger.info(f"Restore verification complete: {parity_percentage}% parity, RTO: {rto_minutes:.1f} minutes")
        
        return {
            "success": True,
            "parity_percentage": parity_percentage,
            "parity_results": parity_results,
            "rto_minutes": rto_minutes,
            "rto_target_met": rto_minutes <= 30,
            "tables_checked": total_tables,
            "tables_matching": matching_tables
        }
    
    except Exception as e:
        logger.error(f"Restore verification error: {e}")
        
        # Cleanup temp database on error
        try:
            conn = psycopg2.connect(
                host=PGHOST,
                port=PGPORT,
                database="postgres",
                user=PGUSER,
                password=PGPASSWORD
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {temp_db_name}")
            cursor.close()
            conn.close()
        except:
            pass
        
        return {
            "success": False,
            "error": str(e)
        }


def run_restore_drill():
    """Run restore drill on most recent backup"""
    try:
        # Find most recent backup
        backups = sorted(BACKUP_DIR.glob("backup_*.sql"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        if not backups:
            return {
                "success": False,
                "error": "No backups found"
            }
        
        latest_backup = backups[0]
        logger.info(f"Running restore drill on {latest_backup}")
        
        result = restore_to_temp_db(latest_backup)
        result["backup_file"] = latest_backup.name
        
        return result
    
    except Exception as e:
        logger.error(f"Restore drill error: {e}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Manual restore drill execution
    result = run_restore_drill()
    if result["success"]:
        print(f"PARITY:{result['parity_percentage']:.0f}%")
        print(f"RTO: {result['rto_minutes']:.1f} minutes")
    else:
        print(f"FAIL: {result['error']}")
