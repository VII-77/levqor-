import json
import os
import logging

log = logging.getLogger(__name__)

FLAGS_FILE = os.path.join(os.path.dirname(__file__), "flags.json")
_FLAGS_CACHE = None

def load_flags():
    """Load feature flags from config/flags.json"""
    global _FLAGS_CACHE
    
    if _FLAGS_CACHE is not None:
        return _FLAGS_CACHE
    
    try:
        with open(FLAGS_FILE, 'r') as f:
            _FLAGS_CACHE = json.load(f)
            log.info(f"Feature flags loaded: {list(_FLAGS_CACHE.keys())}")
            return _FLAGS_CACHE
    except FileNotFoundError:
        log.warning(f"Feature flags file not found: {FLAGS_FILE}")
        return {}
    except Exception as e:
        log.error(f"Error loading feature flags: {e}")
        return {}

def is_enabled(flag_name, default=False):
    """
    Check if a feature flag is enabled
    
    Args:
        flag_name (str): Name of the flag
        default (bool): Default value if flag not found
    
    Returns:
        bool: True if enabled, False otherwise
    """
    flags = load_flags()
    
    env_override = os.environ.get(f"FLAG_{flag_name}")
    if env_override is not None:
        return env_override.lower() in ('true', '1', 'yes', 'on')
    
    return flags.get(flag_name, default)

def get_all_flags():
    """Get all feature flags with their current values"""
    flags = load_flags()
    
    for key in flags.keys():
        env_override = os.environ.get(f"FLAG_{key}")
        if env_override is not None:
            flags[key] = env_override.lower() in ('true', '1', 'yes', 'on')
    
    return flags

def reload_flags():
    """Force reload of feature flags from file"""
    global _FLAGS_CACHE
    _FLAGS_CACHE = None
    return load_flags()
