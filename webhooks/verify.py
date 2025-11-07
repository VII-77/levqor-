"""
Webhook Signature Verification
Supports Stripe, Slack, Telegram, and generic HMAC
"""
import os
import hmac
import hashlib
import time
import logging
from flask import request

logger = logging.getLogger(__name__)

WEBHOOK_VERIFY_ALL = os.getenv("WEBHOOK_VERIFY_ALL", "false").lower() == "true"
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def verify_stripe_webhook(payload: bytes, sig_header: str) -> bool:
    """Verify Stripe webhook signature"""
    if not STRIPE_WEBHOOK_SECRET:
        if WEBHOOK_VERIFY_ALL:
            logger.error("Stripe webhook verification required but STRIPE_WEBHOOK_SECRET not set")
            return False
        return True  # Allow if verification not enforced
    
    try:
        import stripe
        stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        return True
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Stripe signature verification failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Stripe webhook verification error: {e}")
        return False


def verify_slack_webhook(payload: bytes, timestamp: str, signature: str) -> bool:
    """
    Verify Slack webhook signature
    Uses X-Slack-Request-Timestamp and X-Slack-Signature
    """
    if not SLACK_SIGNING_SECRET:
        if WEBHOOK_VERIFY_ALL:
            logger.error("Slack webhook verification required but SLACK_SIGNING_SECRET not set")
            return False
        return True
    
    try:
        # Check timestamp freshness (within 5 minutes)
        current_time = int(time.time())
        if abs(current_time - int(timestamp)) > 300:
            logger.error("Slack webhook timestamp too old")
            return False
        
        # Compute signature
        sig_basestring = f"v0:{timestamp}:{payload.decode('utf-8')}"
        computed_signature = 'v0=' + hmac.new(
            SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        if not hmac.compare_digest(computed_signature, signature):
            logger.error("Slack signature verification failed")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Slack webhook verification error: {e}")
        return False


def verify_telegram_webhook(payload: dict) -> bool:
    """
    Verify Telegram webhook authenticity
    Checks update_id and secret token
    """
    if not TELEGRAM_BOT_TOKEN:
        if WEBHOOK_VERIFY_ALL:
            logger.error("Telegram webhook verification required but TELEGRAM_BOT_TOKEN not set")
            return False
        return True
    
    # Telegram doesn't use signatures, but validates via secret token path
    # The webhook URL should include the bot token
    # This is a basic check - implement token path validation in route
    
    if "update_id" not in payload:
        logger.error("Telegram webhook missing update_id")
        return False
    
    return True


def verify_generic_hmac(payload: bytes, signature: str, secret: str, algorithm: str = "sha256") -> bool:
    """
    Generic HMAC signature verification
    For services like Notion, GitHub, etc.
    """
    if not secret:
        if WEBHOOK_VERIFY_ALL:
            logger.error("Generic webhook verification required but secret not provided")
            return False
        return True
    
    try:
        hash_func = getattr(hashlib, algorithm)
        computed_signature = hmac.new(
            secret.encode(),
            payload,
            hash_func
        ).hexdigest()
        
        # Handle common signature formats
        if signature.startswith(f"{algorithm}="):
            signature = signature.split("=", 1)[1]
        
        if not hmac.compare_digest(computed_signature, signature):
            logger.error("Generic HMAC signature verification failed")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Generic webhook verification error: {e}")
        return False


def verify_webhook(provider: str, payload: bytes, headers: dict) -> bool:
    """
    Main webhook verification dispatcher
    Returns True if verified, False if verification fails
    """
    if not WEBHOOK_VERIFY_ALL:
        return True  # Verification disabled
    
    provider = provider.lower()
    
    if provider == "stripe":
        sig_header = headers.get("Stripe-Signature")
        if not sig_header:
            logger.error("Stripe webhook missing signature header")
            return False
        return verify_stripe_webhook(payload, sig_header)
    
    elif provider == "slack":
        timestamp = headers.get("X-Slack-Request-Timestamp")
        signature = headers.get("X-Slack-Signature")
        if not timestamp or not signature:
            logger.error("Slack webhook missing signature headers")
            return False
        return verify_slack_webhook(payload, timestamp, signature)
    
    elif provider == "telegram":
        try:
            import json
            payload_dict = json.loads(payload)
            return verify_telegram_webhook(payload_dict)
        except Exception as e:
            logger.error(f"Telegram webhook payload parsing failed: {e}")
            return False
    
    elif provider in ["notion", "github"]:
        signature = headers.get("X-Hub-Signature-256") or headers.get("X-Notion-Signature")
        if not signature:
            logger.error(f"{provider} webhook missing signature header")
            return False
        # Need provider-specific secret from env
        secret = os.getenv(f"{provider.upper()}_WEBHOOK_SECRET")
        return verify_generic_hmac(payload, signature, secret)
    
    else:
        logger.warning(f"Unknown webhook provider: {provider}")
        if WEBHOOK_VERIFY_ALL:
            return False  # Reject unknown providers when verification enforced
        return True


def webhook_auth_required(provider: str):
    """
    Decorator for webhook endpoints requiring signature verification
    Usage: @webhook_auth_required("stripe")
    """
    from functools import wraps
    from flask import jsonify
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get raw payload
            payload = request.get_data()
            headers = dict(request.headers)
            
            # Verify signature
            if not verify_webhook(provider, payload, headers):
                return jsonify({
                    "error": "unauthorized",
                    "message": "Webhook signature verification failed"
                }), 401
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
