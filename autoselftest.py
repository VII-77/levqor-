#!/usr/bin/env python3
"""
Levqor Backend Auto Self-Test
Validates core functionality, connectivity, and data integrity.
"""

import sys
import json
import sqlite3
import os
from time import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")
EXIT_FAIL = 1
EXIT_PASS = 0

class SelfTest:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []

    def log(self, msg):
        print(f"[TEST] {msg}")

    def test(self, name, func):
        """Run a test function and track results."""
        self.tests_run += 1
        try:
            self.log(f"Running: {name}")
            func()
            self.tests_passed += 1
            self.log(f"✓ PASS: {name}")
            return True
        except AssertionError as e:
            self.tests_failed += 1
            self.failures.append(f"{name}: {e}")
            self.log(f"✗ FAIL: {name} - {e}")
            return False
        except Exception as e:
            self.tests_failed += 1
            self.failures.append(f"{name}: Unexpected error - {e}")
            self.log(f"✗ ERROR: {name} - {e}")
            return False

    def http_get(self, path, expected_status=200):
        """Make HTTP GET request."""
        url = f"{BACKEND_URL}{path}"
        try:
            req = Request(url)
            with urlopen(req, timeout=10) as response:
                status = response.getcode()
                body = response.read().decode('utf-8')
                assert status == expected_status, f"Expected {expected_status}, got {status}"
                return json.loads(body) if body else {}
        except HTTPError as e:
            if e.code == expected_status:
                return {}
            raise AssertionError(f"HTTP {e.code} from {url}")
        except URLError as e:
            raise AssertionError(f"Network error: {e.reason}")

    def test_health_endpoint(self):
        """Test /health endpoint."""
        data = self.http_get("/health")
        assert data.get("ok") == True, "Health check failed"
        assert "ts" in data, "Missing timestamp"

    def test_ready_endpoint(self):
        """Test /ready endpoint."""
        data = self.http_get("/ready")
        assert data.get("ok") == True, "Ready check failed"
        assert data.get("status") == "ready", "Status not ready"

    def test_status_endpoint(self):
        """Test /status endpoint."""
        data = self.http_get("/status")
        assert data.get("ok") == True, "Status check failed"
        assert data.get("status") == "operational", "Status not operational"

    def test_database_connectivity(self):
        """Test SQLite database connectivity."""
        db_path = os.environ.get("SQLITE_PATH", "levqor.db")
        assert os.path.exists(db_path), f"Database not found: {db_path}"
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check users table
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        assert user_count >= 0, "Users table query failed"
        
        # Check metrics table
        cursor.execute("SELECT COUNT(*) FROM metrics")
        metrics_count = cursor.fetchone()[0]
        assert metrics_count >= 0, "Metrics table query failed"
        
        conn.close()

    def test_metrics_endpoint(self):
        """Test metrics tracking endpoint."""
        data = self.http_get("/api/v1/metrics/summary")
        assert "total" in data, "Missing total metrics"
        assert "last_24h" in data, "Missing 24h metrics"
        assert "conversion_rate" in data, "Missing conversion rate"

    def test_marketing_summary(self):
        """Test marketing summary endpoint."""
        data = self.http_get("/api/v1/marketing/summary")
        assert "visits" in data or "active_users" in data, "Invalid marketing data"

    def test_public_metrics(self):
        """Test public metrics endpoint."""
        data = self.http_get("/public/metrics")
        assert "uptime_rolling_7d" in data, "Missing uptime metric"

    def test_sitemap(self):
        """Test sitemap.xml availability."""
        try:
            req = Request(f"{BACKEND_URL}/public/sitemap.xml")
            with urlopen(req, timeout=10) as response:
                status = response.getcode()
                content = response.read().decode('utf-8')
                assert status == 200, f"Sitemap returned {status}"
                assert "<?xml" in content, "Not valid XML"
                assert "app.levqor.ai" in content, "Missing frontend domain"
        except Exception as e:
            raise AssertionError(f"Sitemap test failed: {e}")

    def test_cors_headers(self):
        """Test CORS headers are present."""
        try:
            req = Request(f"{BACKEND_URL}/health")
            req.add_header("Origin", "https://app.levqor.ai")
            with urlopen(req, timeout=10) as response:
                headers = response.headers
                assert headers.get("Access-Control-Allow-Origin"), "Missing CORS header"
        except Exception as e:
            raise AssertionError(f"CORS test failed: {e}")

    def test_backup_exists(self):
        """Test that backup files exist."""
        backup_dir = "backups"
        assert os.path.exists(backup_dir), "Backup directory missing"
        backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
        assert len(backups) > 0, "No backup files found"

    def run_all(self):
        """Run all tests."""
        print("\n" + "="*80)
        print("LEVQOR BACKEND AUTO SELF-TEST")
        print("="*80 + "\n")

        # API Health Tests
        self.test("Health Endpoint", self.test_health_endpoint)
        self.test("Ready Endpoint", self.test_ready_endpoint)
        self.test("Status Endpoint", self.test_status_endpoint)
        
        # Database Tests
        self.test("Database Connectivity", self.test_database_connectivity)
        
        # Metrics Tests
        self.test("Metrics Summary", self.test_metrics_endpoint)
        self.test("Marketing Summary", self.test_marketing_summary)
        self.test("Public Metrics", self.test_public_metrics)
        
        # Infrastructure Tests
        self.test("Sitemap XML", self.test_sitemap)
        self.test("CORS Headers", self.test_cors_headers)
        self.test("Backup Files", self.test_backup_exists)

        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Tests Run:    {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_failed}")
        
        if self.tests_failed > 0:
            print("\nFAILURES:")
            for failure in self.failures:
                print(f"  - {failure}")
            print("\nStatus: FAIL")
            return EXIT_FAIL
        else:
            print("\nStatus: PASS ✓")
            return EXIT_PASS

if __name__ == "__main__":
    tester = SelfTest()
    sys.exit(tester.run_all())
