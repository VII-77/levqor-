"""
PostgreSQL adapter for Levqor (optional, non-disruptive)
Maintains SQLite as primary, adds Postgres support via env flag
"""

import os
import sqlite3
from typing import Optional, Any

# Check for PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

class DatabaseAdapter:
    """Unified database adapter supporting SQLite and PostgreSQL"""
    
    def __init__(self):
        self.db_type = os.environ.get("DB_TYPE", "sqlite").lower()
        self.conn = None
        
        if self.db_type == "postgres" and not POSTGRES_AVAILABLE:
            print("WARNING: PostgreSQL requested but psycopg2 not installed. Falling back to SQLite.")
            self.db_type = "sqlite"
    
    def connect(self):
        """Establish database connection"""
        if self.db_type == "postgres":
            return self._connect_postgres()
        else:
            return self._connect_sqlite()
    
    def _connect_sqlite(self):
        """Connect to SQLite database"""
        db_path = os.environ.get("SQLITE_PATH", "data/levqor.db")
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    
    def _connect_postgres(self):
        """Connect to PostgreSQL database"""
        if not POSTGRES_AVAILABLE:
            raise RuntimeError("psycopg2 not installed")
        
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL not set for PostgreSQL")
        
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        return conn
    
    def execute(self, query: str, params: tuple = None):
        """Execute query with parameter substitution"""
        if self.db_type == "postgres":
            # Convert ? placeholders to %s for PostgreSQL
            query = query.replace("?", "%s")
        
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor
    
    def commit(self):
        """Commit transaction"""
        self.conn.commit()
    
    def close(self):
        """Close connection"""
        if self.conn:
            self.conn.close()

# Usage example:
# db = DatabaseAdapter()
# conn = db.connect()
# cursor = db.execute("SELECT * FROM users WHERE email = ?", ("user@example.com",))
# db.commit()
