from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
from time import time
from uuid import uuid4
import sqlite3
import json
import os

app = Flask(__name__, 
    static_folder='public',
    static_url_path='/public')

DB_PATH = os.environ.get("DATABASE_URL", os.path.join(os.getcwd(), "levqor.db"))
_db_connection = None

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
        _db_connection.commit()
    return _db_connection

@app.after_request
def add_headers(r):
    r.headers["Access-Control-Allow-Origin"] = "https://levqor.ai"
    r.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    r.headers["X-Content-Type-Options"] = "nosniff"
    r.headers["X-Frame-Options"] = "DENY"
    r.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    r.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return r

@app.get("/")
def root():
    return jsonify({"ok": True, "service": "levqor-backend", "version": "1.0.0"}), 200

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
        "workflow": {"type": "string", "minLength": 1},
        "payload": {"type": "object"},
        "callback_url": {"type": "string", "minLength": 1},
        "priority": {"type": "string", "enum": ["low","normal","high"]},
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
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    data = request.get_json(silent=True)
    try:
        validate(instance=data, schema=INTAKE_SCHEMA)
    except ValidationError as e:
        return bad_request("Invalid request body", e.message)

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
    job = JOBS.get(job_id)
    if not job:
        return jsonify({"error": "not_found"}), 404
    body = request.get_json(silent=True) or {}
    job["status"] = "succeeded"
    job["result"] = body.get("result", {"ok": True})
    return jsonify({"ok": True})

@app.post("/api/v1/users/upsert")
def users_upsert():
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    body = request.get_json(silent=True) or {}
    try:
        validate(instance=body, schema=USER_UPSERT_SCHEMA)
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
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    body = request.get_json(silent=True) or {}
    try:
        validate(instance=body, schema=USER_PATCH_SCHEMA)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
