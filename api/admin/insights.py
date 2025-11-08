from flask import Blueprint, request, jsonify
from monitors.ai_insights import summarize_incident, explain_anomaly, weekly_brief

bp = Blueprint('admin_insights', __name__)

@bp.route('/api/admin/incidents/summarize', methods=['POST'])
def summarize():
    """Generate AI-powered incident summary"""
    return jsonify(summarize_incident(request.json or {}))

@bp.route('/api/admin/anomaly/explain')
def anomaly():
    """Explain detected anomalies with statistical analysis"""
    latency = float(request.args.get('latency_ms', 100))
    return jsonify(explain_anomaly(latency))

@bp.route('/api/admin/brief/weekly')
def brief():
    """Generate weekly operational brief"""
    return jsonify(weekly_brief('7d'))
