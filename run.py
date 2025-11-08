from flask import Flask, request, jsonify, render_template
from jsonschema import validate, ValidationError, FormatChecker
from time import time
from uuid import uuid4
from collections import defaultdict, deque
import sqlite3
import json
import os
import logging
import sys
import jwt
from datetime import datetime, timedelta

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger("levqor")

BUILD = os.environ.get("BUILD_ID", "dev")
VERSION = "1.0.0"
START_TIME = time()

if os.environ.get("SENTRY_DSN"):
    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        sentry_sdk.init(
            dsn=os.environ.get("SENTRY_DSN"),
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=os.environ.get("ENVIRONMENT", "production"),
            release=f"levqor-backend@{VERSION}"
        )
        log.info("Sentry initialized with Flask integration")
    except ImportError:
        log.warning("SENTRY_DSN set but sentry_sdk not installed")
    except Exception as e:
        log.warning(f"Sentry init failed: {e}")

try:
    from monitors.scheduler import get_scheduler
    _scheduler_instance = get_scheduler()
except Exception as e:
    log.warning(f"Scheduler initialization skipped: {e}")

app = Flask(__name__, 
    static_folder='public',
    static_url_path='/public')

# Register Phase 6.4 blueprints
from api.billing.pricing import bp as pricing_bp
from api.admin.ledger import bp as ledger_bp
from api.admin.flags import bp as flags_bp

# Register Phase 6.5 blueprints
from api.admin.growth import bp as growth_admin_bp
from api.billing.discounts import bp as discounts_bp

app.register_blueprint(pricing_bp)
app.register_blueprint(ledger_bp)
app.register_blueprint(flags_bp)
app.register_blueprint(growth_admin_bp)
app.register_blueprint(discounts_bp)

app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_CONTENT_LENGTH", 512 * 1024))

DB_PATH = os.environ.get("SQLITE_PATH", os.path.join(os.getcwd(), "levqor.db"))
_db_connection = None

API_KEYS = set((os.environ.get("API_KEYS") or "").split(",")) - {""}
API_KEYS_NEXT = set((os.environ.get("API_KEYS_NEXT") or "").split(",")) - {""}
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-in-prod")

RATE_BURST = int(os.environ.get("RATE_BURST", 20))
RATE_GLOBAL = int(os.environ.get("RATE_GLOBAL", 200))
WINDOW = 60

_IP_HITS = defaultdict(deque)
_ALL_HITS = deque()
_PROTECTED_PATH_HITS = defaultdict(deque)

def get_db():
    global _db_connection
    if _db_connection is None:
        db_dir = os.path.dirname(DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        _db_connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS users(
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            locale TEXT,
            currency TEXT,
            meta TEXT,
            created_at REAL,
            updated_at REAL
          )
        """)
        _db_connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS referrals(
            id TEXT PRIMARY KEY,
            user_id TEXT,
            email TEXT,
            source TEXT NOT NULL,
            campaign TEXT,
            medium TEXT,
            created_at REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
          )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_referrals_user_id ON referrals(user_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_referrals_source ON referrals(source)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_referrals_created_at ON referrals(created_at)")
        
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS analytics_aggregates(
            day DATE PRIMARY KEY,
            dau INTEGER NOT NULL DEFAULT 0,
            wau INTEGER NOT NULL DEFAULT 0,
            mau INTEGER NOT NULL DEFAULT 0,
            computed_at TEXT NOT NULL
          )
        """)
        
        _db_connection.execute("PRAGMA journal_mode=WAL")
        _db_connection.execute("PRAGMA synchronous=NORMAL")
        _db_connection.commit()
    return _db_connection

def require_key():
    key = request.headers.get("X-Api-Key")
    if not API_KEYS or key in API_KEYS or key in API_KEYS_NEXT:
        return None
    return jsonify({"error": "forbidden"}), 403

def throttle():
    now = time()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
    
    while _ALL_HITS and now - _ALL_HITS[0] > WINDOW:
        _ALL_HITS.popleft()
    dq = _IP_HITS[ip]
    while dq and now - dq[0] > WINDOW:
        dq.popleft()
    
    if len(dq) >= RATE_BURST or len(_ALL_HITS) >= RATE_GLOBAL:
        resp = jsonify({"error": "rate_limited"})
        resp.status_code = 429
        resp.headers["Retry-After"] = "60"
        resp.headers["X-RateLimit-Limit"] = str(RATE_BURST)
        resp.headers["X-RateLimit-Remaining"] = "0"
        resp.headers["X-RateLimit-Reset"] = str(int(now) + WINDOW)
        return resp
    
    dq.append(now)
    _ALL_HITS.append(now)
    return None

def protected_path_throttle():
    protected_prefixes = ['/billing/', '/api/partners/', '/api/admin/', '/api/user/', '/webhooks/']
    if not any(request.path.startswith(prefix) for prefix in protected_prefixes):
        return None
    
    now = time()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
    key = f"protected:{ip}"
    
    dq = _PROTECTED_PATH_HITS[key]
    while dq and now - dq[0] > WINDOW:
        dq.popleft()
    
    if len(dq) >= 60:
        resp = jsonify({"error": "rate_limited"})
        resp.status_code = 429
        resp.headers["Retry-After"] = "60"
        return resp
    
    dq.append(now)
    return None

@app.before_request
def _log_in():
    log.info("in %s %s ip=%s ua=%s", request.method, request.path,
             request.headers.get("X-Forwarded-For", request.remote_addr),
             request.headers.get("User-Agent", "-"))
    
    rate_check = protected_path_throttle()
    if rate_check:
        return rate_check

@app.after_request
def add_headers(r):
    r.headers["Access-Control-Allow-Origin"] = "https://levqor.ai"
    r.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS,PATCH"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Api-Key"
    r.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    r.headers["Content-Security-Policy"] = "default-src 'none'; connect-src https://levqor.ai https://api.levqor.ai; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    r.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    r.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    r.headers["X-Content-Type-Options"] = "nosniff"
    r.headers["X-Frame-Options"] = "DENY"
    r.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    r.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return r

@app.errorhandler(Exception)
def on_error(e):
    log.exception("error: %s", e)
    return jsonify({"error": "internal_error"}), 500

@app.get("/")
def root():
    return jsonify({"ok": True, "service": "levqor-backend", "version": VERSION, "build": BUILD}), 200

@app.get("/health")
def health():
    return jsonify({"ok": True, "ts": int(time())}), 200

@app.get("/status")
def api_status():
    return jsonify({"status": "pass"}), 200

@app.get("/public/metrics")
def public_metrics():
    return jsonify({
        "uptime_rolling_7d": 99.99,
        "jobs_today": 0,
        "audit_coverage": 100,
        "last_updated": int(time())
    })

@app.post("/audit")
def audit():
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    
    data = request.get_json(silent=True)
    if not data:
        return bad_request("Invalid JSON")
    
    event = data.get("event", "unknown")
    email = data.get("email", "unknown")
    ip = data.get("ip", "")
    user_agent = data.get("user_agent", "")
    ts = data.get("ts", int(time() * 1000))
    
    audit_entry = json.dumps({
        "event": event,
        "email": email,
        "ip": ip,
        "user_agent": user_agent,
        "ts": ts
    }, separators=(',', ':'))
    
    audit_file = os.path.join("logs", "audit.log")
    try:
        with open(audit_file, "a") as f:
            f.write(audit_entry + "\n")
    except Exception as e:
        log.warning(f"Failed to write audit log: {e}")
    
    return jsonify({"ok": True}), 200

@app.post("/api/admin/impersonate")
def admin_impersonate():
    admin_token = request.headers.get("X-ADMIN-TOKEN")
    if not ADMIN_TOKEN or admin_token != ADMIN_TOKEN:
        return jsonify({"error": "forbidden"}), 403
    
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    
    data = request.get_json(silent=True)
    if not data or "email" not in data:
        return bad_request("email required")
    
    email = data["email"]
    exp = datetime.utcnow() + timedelta(minutes=15)
    
    token = jwt.encode({
        "email": email,
        "exp": exp,
        "impersonated": True
    }, JWT_SECRET, algorithm="HS256")
    
    audit_entry = json.dumps({
        "event": "admin_impersonate",
        "email": email,
        "admin_ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "ts": int(time() * 1000)
    }, separators=(',', ':'))
    
    audit_file = os.path.join("logs", "audit.log")
    try:
        with open(audit_file, "a") as f:
            f.write(audit_entry + "\n")
    except Exception as e:
        log.warning(f"Failed to write audit log: {e}")
    
    return jsonify({"token": token}), 200

JOBS = {}

INTAKE_SCHEMA = {
    "type": "object",
    "properties": {
        "workflow": {"type": "string", "minLength": 1, "maxLength": 128},
        "payload": {"type": "object"},
        "callback_url": {"type": "string", "minLength": 1, "maxLength": 1024},
        "priority": {"type": "string", "enum": ["low", "normal", "high"]},
    },
    "required": ["workflow", "payload"],
    "additionalProperties": False,
}

STATUS_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["queued","running","succeeded","failed"]},
        "created_at": {"type": "number"},
        "result": {},
        "error": {},
    },
    "required": ["status","created_at"],
    "additionalProperties": True,
}

USER_UPSERT_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "minLength": 3},
        "name": {"type": "string"},
        "locale": {"type": "string"},
        "currency": {"type": "string", "enum": ["GBP", "USD", "EUR"]},
        "meta": {"type": "object"}
    },
    "required": ["email"],
    "additionalProperties": False
}

USER_PATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "locale": {"type": "string"},
        "currency": {"type": "string", "enum": ["GBP", "USD", "EUR"]},
        "meta": {"type": "object"}
    },
    "additionalProperties": False
}

def bad_request(message, details=None):
    return jsonify({"error": message, "details": details}), 400

def row_to_user(row):
    if not row:
        return None
    (id_, email, name, locale, currency, meta, created_at, updated_at) = row
    return {
        "id": id_,
        "email": email,
        "name": name,
        "locale": locale,
        "currency": currency,
        "meta": json.loads(meta) if meta else {},
        "created_at": created_at,
        "updated_at": updated_at
    }

def fetch_user_by_email(email):
    cur = get_db().execute("SELECT id,email,name,locale,currency,meta,created_at,updated_at FROM users WHERE email = ?", (email,))
    return row_to_user(cur.fetchone())

def fetch_user_by_id(uid):
    cur = get_db().execute("SELECT id,email,name,locale,currency,meta,created_at,updated_at FROM users WHERE id = ?", (uid,))
    return row_to_user(cur.fetchone())

@app.post("/api/v1/intake")
def intake():
    guard = require_key()
    if guard:
        return guard
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    data = request.get_json(silent=True)
    if data is None:
        return bad_request("Invalid JSON")
    try:
        validate(instance=data, schema=INTAKE_SCHEMA, format_checker=FormatChecker())
    except ValidationError as e:
        return bad_request("Invalid request body", e.message)
    
    if len(json.dumps(data["payload"])) > 200 * 1024:
        return bad_request("payload too large")
    
    if "callback_url" in data:
        url = data["callback_url"]
        if not url.startswith(("http://", "https://")):
            return bad_request("callback_url must be a valid HTTP(S) URL")

    job_id = uuid4().hex
    JOBS[job_id] = {
        "status": "queued",
        "created_at": time(),
        "input": data,
        "result": None,
        "error": None,
    }

    return jsonify({"job_id": job_id, "status": "queued"}), 202

@app.get("/api/v1/status/<job_id>")
def status(job_id):
    job = JOBS.get(job_id)
    if not job:
        return jsonify({"error": "not_found", "job_id": job_id}), 404

    public_view = {
        "status": job["status"],
        "created_at": job["created_at"],
        "result": job["result"],
        "error": job["error"],
    }
    try:
        validate(instance=public_view, schema=STATUS_SCHEMA)
    except ValidationError:
        pass

    return jsonify({"job_id": job_id, **public_view}), 200

@app.post("/api/v1/_dev/complete/<job_id>")
def dev_complete(job_id):
    guard = require_key()
    if guard:
        return guard
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    job = JOBS.get(job_id)
    if not job:
        return jsonify({"error": "not_found"}), 404
    body = request.get_json(silent=True) or {}
    job["status"] = "succeeded"
    job["result"] = body.get("result", {"ok": True})
    return jsonify({"ok": True})

@app.post("/api/v1/users/upsert")
def users_upsert():
    guard = require_key()
    if guard:
        return guard
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    body = request.get_json(silent=True) or {}
    try:
        validate(instance=body, schema=USER_UPSERT_SCHEMA, format_checker=FormatChecker())
    except ValidationError as e:
        return bad_request("Invalid user payload", e.message)

    now = time()
    email = body["email"].strip().lower()
    name = body.get("name")
    locale = body.get("locale")
    currency = body.get("currency")
    meta = json.dumps(body.get("meta", {}))

    existing = fetch_user_by_email(email)
    if existing:
        get_db().execute(
            "UPDATE users SET name=?, locale=?, currency=?, meta=?, updated_at=? WHERE email=?",
            (name, locale, currency, meta, now, email)
        )
        get_db().commit()
        return jsonify({"updated": True, "user": fetch_user_by_email(email)}), 200
    else:
        uid = uuid4().hex
        get_db().execute(
            "INSERT INTO users(id,email,name,locale,currency,meta,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
            (uid, email, name, locale, currency, meta, now, now)
        )
        get_db().commit()
        return jsonify({"created": True, "user": fetch_user_by_id(uid)}), 201

@app.patch("/api/v1/users/<user_id>")
def users_patch(user_id):
    guard = require_key()
    if guard:
        return guard
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    body = request.get_json(silent=True) or {}
    try:
        validate(instance=body, schema=USER_PATCH_SCHEMA, format_checker=FormatChecker())
    except ValidationError as e:
        return bad_request("Invalid patch payload", e.message)

    u = fetch_user_by_id(user_id)
    if not u:
        return jsonify({"error": "not_found", "user_id": user_id}), 404

    name = body.get("name", u["name"])
    locale = body.get("locale", u["locale"])
    currency = body.get("currency", u["currency"])
    meta = u["meta"].copy()
    meta.update(body.get("meta", {}))
    get_db().execute(
        "UPDATE users SET name=?, locale=?, currency=?, meta=?, updated_at=? WHERE id=?",
        (name, locale, currency, json.dumps(meta), time(), user_id)
    )
    get_db().commit()
    return jsonify({"updated": True, "user": fetch_user_by_id(user_id)}), 200

@app.get("/api/v1/users/<user_id>")
def users_get(user_id):
    u = fetch_user_by_id(user_id)
    if not u:
        return jsonify({"error": "not_found", "user_id": user_id}), 404
    return jsonify(u), 200

@app.post("/api/v1/referrals/track")
def track_referral():
    """Track a referral source (public endpoint for analytics)"""
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()
    source = body.get("source", "direct").strip()
    campaign = body.get("campaign", "").strip()
    medium = body.get("medium", "").strip()
    
    if not email or not source:
        return jsonify({"error": "email and source required"}), 400
    
    user = fetch_user_by_email(email)
    user_id = user["id"] if user else None
    
    referral_id = uuid4().hex
    now = time()
    
    get_db().execute(
        "INSERT INTO referrals(id, user_id, email, source, campaign, medium, created_at) VALUES (?,?,?,?,?,?,?)",
        (referral_id, user_id, email, source, campaign, medium, now)
    )
    get_db().commit()
    
    return jsonify({"ok": True, "referral_id": referral_id}), 201

@app.get("/admin/analytics")
def admin_analytics():
    """Get retention and referral analytics (requires admin token)"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "unauthorized"}), 401
    
    token = auth_header.split(" ")[1]
    if token != ADMIN_TOKEN:
        return jsonify({"error": "forbidden"}), 403
    
    now = time()
    seven_days_ago = now - (7 * 24 * 60 * 60)
    thirty_days_ago = now - (30 * 24 * 60 * 60)
    
    db = get_db()
    
    cursor = db.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor = db.execute("SELECT COUNT(*) FROM users WHERE created_at >= ?", (seven_days_ago,))
    new_users_7d = cursor.fetchone()[0]
    
    cursor = db.execute("SELECT COUNT(*) FROM users WHERE created_at >= ?", (thirty_days_ago,))
    new_users_30d = cursor.fetchone()[0]
    
    cursor = db.execute("""
        SELECT source, COUNT(*) as count 
        FROM referrals 
        WHERE created_at >= ? 
        GROUP BY source 
        ORDER BY count DESC 
        LIMIT 10
    """, (thirty_days_ago,))
    top_referrals = [{"source": row[0], "count": row[1]} for row in cursor.fetchall()]
    
    cursor = db.execute("SELECT COUNT(*) FROM referrals WHERE created_at >= ?", (seven_days_ago,))
    referrals_7d = cursor.fetchone()[0]
    
    cursor = db.execute("SELECT COUNT(*) FROM referrals WHERE created_at >= ?", (thirty_days_ago,))
    referrals_30d = cursor.fetchone()[0]
    
    return jsonify({
        "users": {
            "total": total_users,
            "new_7d": new_users_7d,
            "new_30d": new_users_30d,
        },
        "referrals": {
            "total_7d": referrals_7d,
            "total_30d": referrals_30d,
            "top_sources": top_referrals
        },
        "timestamp": int(now)
    }), 200

@app.get("/api/v1/users")
def users_lookup():
    email = request.args.get("email", "").strip().lower()
    if not email:
        return bad_request("email query param required")
    u = fetch_user_by_email(email)
    if not u:
        return jsonify({"error": "not_found", "email": email}), 404
    return jsonify(u), 200

@app.get("/api/v1/ops/health")
def ops_health():
    guard = require_key()
    if guard:
        return guard
    return jsonify({"ok": True, "ts": int(time())}), 200

@app.get("/ops/uptime")
def ops_uptime():
    """Public endpoint for system uptime metrics"""
    uptime_seconds = int(time() - START_TIME)
    return jsonify({
        "uptime_seconds": uptime_seconds,
        "start_time": int(START_TIME),
        "current_time": int(time()),
        "version": VERSION,
        "build": BUILD
    }), 200

@app.get("/ops/queue_health")
def ops_queue_health():
    """Public endpoint for job queue health monitoring"""
    queued = sum(1 for j in JOBS.values() if j["status"] == "queued")
    running = sum(1 for j in JOBS.values() if j["status"] == "running")
    completed = sum(1 for j in JOBS.values() if j["status"] == "succeeded")
    failed = sum(1 for j in JOBS.values() if j["status"] == "failed")
    total = len(JOBS)
    
    return jsonify({
        "healthy": True,
        "queue_stats": {
            "queued": queued,
            "running": running,
            "completed": completed,
            "failed": failed,
            "total": total
        },
        "timestamp": int(time())
    }), 200

@app.get("/billing/health")
def billing_health():
    """Public endpoint to verify Stripe integration health"""
    stripe_key = os.environ.get("STRIPE_SECRET_KEY", "")
    stripe_webhook = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    
    has_stripe_key = bool(stripe_key and stripe_key.startswith("sk_"))
    has_webhook_secret = bool(stripe_webhook and len(stripe_webhook) > 10)
    
    healthy = has_stripe_key and has_webhook_secret
    
    return jsonify({
        "healthy": healthy,
        "stripe_key_configured": has_stripe_key,
        "webhook_secret_configured": has_webhook_secret,
        "timestamp": int(time())
    }), 200 if healthy else 503

@app.get("/ops/autoscale/dryrun")
def autoscale_dryrun():
    """Dry-run autoscale decision based on current metrics"""
    from monitors.autoscale import get_controller
    
    queue_depth = int(request.args.get("queue_depth", 0))
    p95_latency = float(request.args.get("p95_latency_ms", 0))
    error_rate = float(request.args.get("error_rate", 0))
    
    controller = get_controller()
    decision = controller.decide_action(queue_depth, p95_latency, error_rate)
    
    return jsonify(decision), 200

@app.post("/ops/autoscale/apply")
def autoscale_apply():
    """Apply autoscale action"""
    from monitors.autoscale import get_controller
    
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    data = request.get_json() or {}
    queue_depth = int(data.get("queue_depth", 0))
    p95_latency = float(data.get("p95_latency_ms", 0))
    error_rate = float(data.get("error_rate", 0))
    
    controller = get_controller()
    decision = controller.decide_action(queue_depth, p95_latency, error_rate)
    result = controller.apply_action(decision)
    
    return jsonify(result), 200

@app.post("/ops/recover")
def ops_recover():
    """Execute incident recovery"""
    from monitors.incident_response import get_responder
    
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    data = request.get_json() or {}
    error_rate = float(data.get("error_rate", 0))
    recent_failures = int(data.get("recent_failures", 0))
    dry_run = bool(data.get("dry_run", False))
    
    responder = get_responder()
    result = responder.recover(error_rate, recent_failures, dry_run)
    
    return jsonify(result), 200

@app.get("/admin/retention")
def admin_retention():
    """Get retention metrics (DAU/WAU/MAU)"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT day, dau, wau, mau, computed_at
        FROM analytics_aggregates
        ORDER BY day DESC
        LIMIT 30
    """)
    
    rows = cursor.fetchall()
    metrics = [
        {
            "day": row[0],
            "dau": row[1],
            "wau": row[2],
            "mau": row[3],
            "computed_at": row[4]
        }
        for row in rows
    ]
    
    return jsonify({
        "ok": True,
        "metrics": metrics,
        "count": len(metrics)
    }), 200

@app.get("/ops/cost/forecast")
def cost_forecast():
    """Get 30-day cost forecast"""
    from scripts.cost_predict import load_cached_forecast, forecast_next_30d
    from scripts.cost_predict import get_stripe_charges_last_30d, estimate_infra_costs, estimate_openai_usage
    
    cached = load_cached_forecast()
    if cached:
        return jsonify(cached), 200
    
    stripe_charges = get_stripe_charges_last_30d()
    infra = estimate_infra_costs()
    openai = estimate_openai_usage()
    
    forecast = forecast_next_30d(stripe_charges, infra, openai)
    
    return jsonify(forecast), 200

OPENAPI = {
    "openapi": "3.0.0",
    "info": {"title": "Levqor API", "version": VERSION},
    "paths": {
        "/api/v1/intake": {"post": {"summary": "Submit job", "responses": {"202": {"description": "Queued"}}}},
        "/api/v1/status/{job_id}": {"get": {"summary": "Get status", "responses": {"200": {"description": "OK"}}}},
        "/api/v1/users/upsert": {"post": {"summary": "Create or update user", "responses": {"201": {"description": "Created"}}}},
        "/api/v1/users/{user_id}": {"get": {"summary": "Get user by ID", "responses": {"200": {"description": "OK"}}}},
        "/api/v1/users": {"get": {"summary": "Lookup user by email", "responses": {"200": {"description": "OK"}}}}
    }
}

@app.get("/public/openapi.json")
def openapi():
    return jsonify(OPENAPI)

@app.get("/ops/anomaly_ai")
def anomaly_ai():
    """ML-based anomaly detection for latency"""
    from monitors.anomaly_ai import predict
    
    try:
        latency_ms = float(request.args.get("latency_ms", "120"))
    except ValueError:
        latency_ms = 120.0
    
    result = predict(latency_ms)
    return jsonify(result), 200

@app.get("/ops/auto_tune")
def auto_tune():
    """Auto-tuning suggestions for SLO targets"""
    from monitors.auto_tune import suggest_tuning
    
    try:
        current_p95 = float(request.args.get("current_p95", "80"))
        current_queue = int(request.args.get("current_queue", "1"))
    except ValueError:
        current_p95 = 80.0
        current_queue = 1
    
    result = suggest_tuning(current_p95, current_queue)
    return jsonify(result), 200

@app.get("/admin/flags")
def admin_flags_ui():
    """Feature flags admin UI"""
    token = (request.headers.get("Authorization") or "").replace("Bearer ", "")
    if not token or token != ADMIN_TOKEN:
        return ("Unauthorized", 401)
    
    return render_template("admin/flags.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
