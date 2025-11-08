from flask import Blueprint, request, jsonify
from monitors.ai_insights import summarize_incident, explain_anomaly, weekly_brief
import logging

log = logging.getLogger("levqor.insights")
bp = Blueprint('admin_insights', __name__)

@bp.route('/api/admin/incidents/summarize', methods=['POST'])
def summarize():
    """Generate AI-powered incident summary"""
    log.info("insights: incidents/summarize called")
    return jsonify(summarize_incident(request.json or {}))

@bp.route('/api/admin/anomaly/explain')
def anomaly():
    """Explain detected anomalies with statistical analysis"""
    log.info("insights: anomaly/explain called with latency=%s", request.args.get('latency_ms'))
    latency = float(request.args.get('latency_ms', 100))
    return jsonify(explain_anomaly(latency))

@bp.route('/api/admin/brief/weekly')
def brief():
    """Generate weekly operational brief"""
    log.info("insights: brief/weekly called")
    return jsonify(weekly_brief('7d'))
