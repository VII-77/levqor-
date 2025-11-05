import os, requests, sys
base = os.environ.get("BASE_URL")
if not base:
    print("Set BASE_URL to your Repl URL, e.g. https://<name>.<user>.repl.co"); sys.exit(1)
def get(p): return requests.get(base+p, timeout=10)
def post(p, j): return requests.post(base+p, json=j, timeout=10)
assert get("/health").status_code == 200
assert get("/public/metrics").status_code == 200
r = post("/api/v1/intake", {"workflow":"demo.flow","payload":{"x":1},"priority":"normal"})
assert r.status_code in (200,202)
job_id = r.json()["job_id"]
assert get(f"/api/v1/status/{job_id}").status_code == 200
print("🟢 COCKPIT GREEN — Levqor backend validated")
