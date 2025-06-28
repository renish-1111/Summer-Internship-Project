# Routes package initialization
import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    from .api_routes import api_bp
except ImportError as e:
    logger.error(f"Failed to import api_bp: {e}")
    raise

try:
    from .pdf_routes import pdf_bp
except ImportError as e:
    logger.error(f"Failed to import pdf_bp: {e}")
    raise

# Export blueprints for easy import
__all__ = ['api_bp', 'pdf_bp']


