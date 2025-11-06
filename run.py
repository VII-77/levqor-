from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError, FormatChecker
from time import time
from uuid import uuid4
from collections import defaultdict, deque
import sqlite3
import json
import os
import logging
import sys
import stripe
import notifier

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger("levqor")

app = Flask(__name__, 
    static_folder='public',
    static_url_path='/public')

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_CONTENT_LENGTH", 512 * 1024))

BUILD = os.environ.get("BUILD_ID", "dev")
VERSION = "1.0.0"

DB_PATH = os.environ.get("SQLITE_PATH", os.path.join(os.getcwd(), "levqor.db"))
_db_connection = None

API_KEYS = set((os.environ.get("API_KEYS") or "").split(",")) - {""}
API_KEYS_NEXT = set((os.environ.get("API_KEYS_NEXT") or "").split(",")) - {""}

RATE_BURST = int(os.environ.get("RATE_BURST", 20))
RATE_GLOBAL = int(os.environ.get("RATE_GLOBAL", 200))
WINDOW = 60

_IP_HITS = defaultdict(deque)
_ALL_HITS = deque()

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

@app.before_request
def _log_in():
    log.info("in %s %s ip=%s ua=%s", request.method, request.path,
             request.headers.get("X-Forwarded-For", request.remote_addr),
             request.headers.get("User-Agent", "-"))

@app.after_request
def add_headers(r):
    if request.path == "/billing/webhook":
        return r
    r.headers["Access-Control-Allow-Origin"] = "https://levqor.ai"
    r.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS,PATCH"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Api-Key"
    r.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    r.headers["Content-Security-Policy"] = "default-src 'none'; connect-src https://levqor.ai https://api.levqor.ai https://checkout.stripe.com https://js.stripe.com; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
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

@app.get("/public/metrics")
def public_metrics():
    return jsonify({
        "uptime_rolling_7d": 99.99,
        "jobs_today": 0,
        "audit_coverage": 100,
        "last_updated": int(time())
    })

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

@app.post("/billing/create-checkout-session")
def create_checkout_session():
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    try:
        replit_domain = os.environ.get("REPLIT_DEV_DOMAIN")
        if not replit_domain:
            domains = os.environ.get("REPLIT_DOMAINS", "")
            replit_domain = domains.split(",")[0] if domains else "levqor-backend.replit.app"
        
        body = request.get_json(silent=True) or {}
        price_id = body.get("price_id")
        user_email = body.get("email")
        user_id = body.get("user_id")
        
        session_params = {
            "line_items": [{
                "price": price_id or "price_1234567890",
                "quantity": 1,
            }],
            "mode": "payment",
            "success_url": f"https://{replit_domain}/success?session_id={{CHECKOUT_SESSION_ID}}",
            "cancel_url": f"https://{replit_domain}/cancel",
        }
        
        if user_email:
            session_params["customer_email"] = user_email
        if user_id:
            session_params["client_reference_id"] = user_id
            session_params["metadata"] = {"user_id": user_id}
        
        checkout_session = stripe.checkout.Session.create(**session_params)
        
        return jsonify({"sessionId": checkout_session.id, "url": checkout_session.url}), 200
        
    except Exception as e:
        log.exception("Stripe checkout error")
        return jsonify({"error": str(e)}), 400

@app.post("/billing/webhook")
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    
    if webhook_secret:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError:
            log.warning("Invalid Stripe webhook payload")
            return jsonify({"error": "invalid_payload"}), 400
        except stripe.error.SignatureVerificationError:
            log.warning("Invalid Stripe webhook signature")
            return jsonify({"error": "invalid_signature"}), 400
    else:
        event = json.loads(payload)
    
    event_type = event.get("type")
    log.info(f"Stripe webhook received: {event_type}")
    
    if event_type == "checkout.session.completed":
        session = event["data"]["object"]
        handle_successful_payment(session)
    elif event_type == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]
        handle_successful_payment(session)
    elif event_type == "checkout.session.async_payment_failed":
        session = event["data"]["object"]
        handle_failed_payment(session)
    
    return jsonify({"received": True}), 200

def handle_successful_payment(session):
    """Process successful payment and send confirmation email"""
    try:
        user_id = session.get("client_reference_id")
        email = session.get("customer_details", {}).get("email") or session.get("customer_email")
        amount_total = session.get("amount_total", 0)
        session_id = session.get("id")
        
        amount_display = f"${amount_total / 100:.2f}" if amount_total else "N/A"
        
        log.info(f"Payment successful: session={session_id}, user={user_id}, email={email}, amount={amount_display}")
        
        if email:
            subject = "Payment Confirmation - Levqor"
            message = f"""Thank you for your payment!

Payment Details:
- Amount: {amount_display}
- Session ID: {session_id}
- User ID: {user_id or 'N/A'}

Your payment has been processed successfully.

If you have any questions, contact us at support@levqor.ai

Best regards,
The Levqor Team
"""
            
            status, response = notifier.send_email(
                to=email,
                subject=subject,
                text=message,
                from_addr="billing@levqor.ai"
            )
            log.info(f"Payment confirmation email sent: status={status}")
        
        if user_id:
            user = fetch_user_by_id(user_id)
            if user:
                meta = user.get("meta", {})
                meta["last_payment"] = {
                    "session_id": session_id,
                    "amount": amount_total,
                    "timestamp": time()
                }
                get_db().execute(
                    "UPDATE users SET meta=?, updated_at=? WHERE id=?",
                    (json.dumps(meta), time(), user_id)
                )
                get_db().commit()
                log.info(f"User {user_id} payment recorded in database")
    
    except Exception as e:
        log.exception(f"Error handling successful payment: {e}")

def handle_failed_payment(session):
    """Handle failed payment"""
    try:
        email = session.get("customer_details", {}).get("email") or session.get("customer_email")
        session_id = session.get("id")
        
        log.warning(f"Payment failed: session={session_id}, email={email}")
        
        if email:
            subject = "Payment Failed - Levqor"
            message = f"""Your payment could not be processed.

Session ID: {session_id}

Please try again or contact support@levqor.ai for assistance.

Best regards,
The Levqor Team
"""
            notifier.send_email(
                to=email,
                subject=subject,
                text=message,
                from_addr="billing@levqor.ai"
            )
    except Exception as e:
        log.exception(f"Error handling failed payment: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
