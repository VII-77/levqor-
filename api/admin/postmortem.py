from flask import Blueprint, request, jsonify
import datetime

bp = Blueprint('admin_postmortem', __name__)

@bp.route('/api/admin/postmortem', methods=['POST'])
def gen_post():
    """Generate automated postmortem report"""
    data = request.get_json(force=True) or {}
    inc = data.get('incident', {})
    md = f"""# Postmortem Report
Date: {datetime.datetime.utcnow().isoformat()}
Summary: {inc.get('summary', 'N/A')}
Severity: {inc.get('severity', 'unknown')}
Resolution: {inc.get('resolution_note', 'Pending')}
"""
    return jsonify({"md": md, "generated_at": datetime.datetime.utcnow().isoformat()})
