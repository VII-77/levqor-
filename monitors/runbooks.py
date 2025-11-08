import os, json, subprocess

RUNBOOKS = {
    "restart_worker": "touch /tmp/restart_worker",
    "flush_dlq": "echo DLQ flushed",
    "rebuild_indexes": "VACUUM; ANALYZE;",
    "toggle_readonly": "echo Maintenance mode toggled"
}

def list_runbooks():
    """List all available runbooks"""
    return list(RUNBOOKS.keys())

def apply_runbook(key, apply=False):
    """Execute or preview a runbook action"""
    if key not in RUNBOOKS:
        return {"error": "unknown runbook"}
    
    if not apply:
        return {"dry_run": True, "action": RUNBOOKS[key]}
    
    os.system(RUNBOOKS[key])
    return {"applied": True, "action": RUNBOOKS[key]}
