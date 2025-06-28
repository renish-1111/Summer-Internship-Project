import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    from .resume import (
        clean_json_response,
        extract_basic_info_fallback,
        is_valid_email,
        is_valid_phone
    )
except ImportError as e:
    logger.error(f"Failed to import resume validation functions: {e}")
    raise

try:
    from .upload import allowed_file
except ImportError as e:
    logger.error(f"Failed to import upload validation functions: {e}")
    raise

# Export functions for easy import
__all__ = [
    "clean_json_response",
    "extract_basic_info_fallback", 
    "is_valid_email",
    "is_valid_phone",
    "allowed_file"
]