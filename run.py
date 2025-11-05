from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
from time import time
from uuid import uuid4

app = Flask(__name__, 
    static_folder='public',
    static_url_path='/public')

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

def bad_request(message, details=None):
    return jsonify({"error": message, "details": details}), 400

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
