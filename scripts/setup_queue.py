#!/usr/bin/env python3
"""
Redis Queue Setup Script
Configures and verifies Redis + RQ queue system for async job processing
"""

import os
import sys
import argparse

def check_redis_connection():
    """Check if Redis is available"""
    try:
        import redis
        r = redis.Redis(
            host=os.environ.get('REDIS_HOST', 'localhost'),
            port=int(os.environ.get('REDIS_PORT', 6379)),
            decode_responses=True
        )
        r.ping()
        print("✅ Redis connection successful")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def verify_rq_worker():
    """Check if RQ worker module is available"""
    try:
        from job_queue import tasks, worker
        print("✅ RQ worker module available")
        return True
    except ImportError as e:
        print(f"❌ RQ worker module missing: {e}")
        return False

def setup_async_mode():
    """Configure system for async queue processing"""
    print("\n🔧 Setting up async queue mode...")
    
    # Check dependencies
    redis_ok = check_redis_connection()
    worker_ok = verify_rq_worker()
    
    if not redis_ok:
        print("\n⚠️  Redis not available. Options:")
        print("  1. Install Redis locally: apt-get install redis-server")
        print("  2. Use Upstash Redis (free tier): https://upstash.com")
        print("  3. Set REDIS_URL environment variable")
        print("\n  System will run in synchronous mode (degraded)")
        return False
    
    if not worker_ok:
        print("\n⚠️  Worker module not found. Install dependencies:")
        print("  pip install rq redis")
        return False
    
    # Enable queue in feature flags
    try:
        import json
        flags_file = "config/flags.json"
        with open(flags_file, 'r') as f:
            flags = json.load(f)
        
        flags['NEW_QUEUE_ENABLED'] = True
        
        with open(flags_file, 'w') as f:
            json.dump(flags, f, indent=2)
        
        print("✅ Feature flag NEW_QUEUE_ENABLED set to true")
    except Exception as e:
        print(f"⚠️  Could not update feature flags: {e}")
    
    print("\n✅ Async queue mode configured!")
    print("\n📋 Next steps:")
    print("  1. Start RQ worker: python -m job_queue.worker")
    print("  2. Restart backend: replit restart")
    print("  3. Verify: curl http://localhost:5000/ops/queue_health")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Setup Redis queue")
    parser.add_argument('--mode', choices=['async', 'check'], default='check',
                       help='Mode: check (verify only) or async (enable queue)')
    args = parser.parse_args()
    
    print("🚀 Redis Queue Setup")
    print("=" * 50)
    
    if args.mode == 'check':
        print("\n📋 Checking queue infrastructure...")
        redis_ok = check_redis_connection()
        worker_ok = verify_rq_worker()
        
        if redis_ok and worker_ok:
            print("\n✅ Queue system ready for async mode")
            return 0
        else:
            print("\n⚠️  Queue system not fully configured (will use sync mode)")
            return 1
    
    elif args.mode == 'async':
        success = setup_async_mode()
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
