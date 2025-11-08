from flask import Blueprint, request, jsonify
from monitors.runbooks import list_runbooks, apply_runbook

bp = Blueprint('admin_runbooks', __name__)

@bp.route('/api/admin/runbooks')
def list_rb():
    """List all available operational runbooks"""
    return jsonify({"runbooks": list_runbooks()})

@bp.route('/api/admin/runbooks/apply', methods=['POST'])
def apply_rb():
    """Apply a runbook action (dry-run or execute)"""
    data = request.json or {}
    return jsonify(apply_runbook(data.get('key'), data.get('apply', False)))
