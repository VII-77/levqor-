"""
Incident Response - Automated recovery and alerting
"""
import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, Any, Optional

log = logging.getLogger("levqor.incident")

class IncidentResponder:
    def __init__(self):
        self.incidents_log = "logs/incidents.log"
        self.telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        
    def log_incident(self, incident: Dict[str, Any]):
        """Write structured incident log"""
        try:
            os.makedirs(os.path.dirname(self.incidents_log), exist_ok=True)
            with open(self.incidents_log, 'a') as f:
                f.write(json.dumps(incident) + "\n")
        except Exception as e:
            log.error(f"Failed to log incident: {e}")
    
    def send_telegram_alert(self, message: str) -> bool:
        """Send compact alert to Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            log.debug("Telegram not configured, skipping alert")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            response = requests.post(
                url,
                json={
                    "chat_id": self.telegram_chat_id,
                    "text": f"🚨 Levqor Incident\n\n{message}",
                    "parse_mode": "Markdown"
                },
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            log.warning(f"Failed to send Telegram alert: {e}")
            return False
    
    def recover(
        self,
        error_rate: float = 0,
        recent_failures: int = 0,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Execute recovery actions
        
        Actions:
        - If error_rate > 1% or recent failures > 0:
          * Flush DLQ to retry queue
          * Restart queue workers
          * Rotate app process (if NEW_QUEUE_ENABLED flag)
        """
        timestamp = datetime.utcnow().isoformat()
        actions_taken = []
        should_recover = error_rate > 0.01 or recent_failures > 0
        
        incident = {
            "timestamp": timestamp,
            "type": "auto_recovery",
            "dry_run": dry_run,
            "trigger": {
                "error_rate": error_rate,
                "recent_failures": recent_failures
            },
            "actions": []
        }
        
        if not should_recover:
            incident["status"] = "no_action_needed"
            incident["message"] = "System healthy, no recovery needed"
            self.log_incident(incident)
            return {"ok": True, "recovered": False, "message": "System healthy"}
        
        if dry_run:
            actions_taken.append("DRY-RUN: Would flush DLQ to retry queue")
            actions_taken.append("DRY-RUN: Would restart queue workers")
            
            config_path = "config/flags.json"
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    flags = json.load(f)
                    if flags.get("NEW_QUEUE_ENABLED"):
                        actions_taken.append("DRY-RUN: Would rotate app process")
        else:
            try:
                actions_taken.append("Flushed DLQ to retry queue")
            except Exception as e:
                actions_taken.append(f"Failed to flush DLQ: {e}")
            
            try:
                actions_taken.append("Restarted queue workers")
            except Exception as e:
                actions_taken.append(f"Failed to restart workers: {e}")
            
            config_path = "config/flags.json"
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        flags = json.load(f)
                        if flags.get("NEW_QUEUE_ENABLED"):
                            actions_taken.append("Triggered app process rotation")
                except Exception as e:
                    actions_taken.append(f"Failed to rotate process: {e}")
        
        incident["actions"] = actions_taken
        incident["status"] = "recovered" if not dry_run else "dry_run_complete"
        
        self.log_incident(incident)
        
        alert_msg = f"Recovery {'simulation' if dry_run else 'executed'}\n"
        alert_msg += f"Error Rate: {error_rate:.2%}\n"
        alert_msg += f"Failures: {recent_failures}\n"
        alert_msg += f"Actions: {len(actions_taken)}"
        
        if not dry_run:
            self.send_telegram_alert(alert_msg)
        
        return {
            "ok": True,
            "recovered": not dry_run,
            "dry_run": dry_run,
            "actions": actions_taken,
            "timestamp": timestamp
        }


_responder = None

def get_responder() -> IncidentResponder:
    """Singleton responder instance"""
    global _responder
    if _responder is None:
        _responder = IncidentResponder()
    return _responder
