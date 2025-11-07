"""
Sentry Initialization
Activates when SENTRY_DSN is set
"""
import os
import logging

logger = logging.getLogger(__name__)

SENTRY_DSN = os.getenv("SENTRY_DSN")


def init_sentry(app=None):
    """Initialize Sentry error tracking"""
    if not SENTRY_DSN:
        logger.info("Sentry disabled (SENTRY_DSN not set)")
        return False
    
    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration
        
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                FlaskIntegration(),
                LoggingIntegration(
                    level=logging.INFO,
                    event_level=logging.ERROR
                )
            ],
            traces_sample_rate=0.1,  # Sample 10% of transactions
            profiles_sample_rate=0.1,
            environment=os.getenv("ENVIRONMENT", "production"),
            release=os.getenv("REPLIT_DEPLOYMENT_ID", "development")
        )
        
        logger.info("Sentry initialized successfully")
        return True
    
    except ImportError:
        logger.warning("sentry-sdk not installed, error tracking disabled")
        return False
    except Exception as e:
        logger.error(f"Sentry initialization failed: {e}")
        return False
