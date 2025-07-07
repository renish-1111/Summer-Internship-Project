import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    from .genAi import load_gemini_model, prompt
except ImportError as e:
    logger.error(f"Failed to import genAi functions: {e}")
    raise

try:
    from .pdfDataExtrection import pdf_to_text
except ImportError as e:
    logger.error(f"Failed to import pdf_to_text: {e}")
    raise

try:
    from .resume_store import resume_store_data
except ImportError as e:
    logger.error(f"Failed to import resume_store_data: {e}")
    raise

try:
    from .cover_letter import generate_cover_letter
except ImportError as e:
    logger.error(f"Failed to import generate_cover_letter: {e}")
    raise

try:
    from .ats import generate_ats_score
except ImportError as e:
    logger.error(f"Failed to import generate_ats_score: {e}")
    raise

# Export all functions for easy import
__all__ = ['load_gemini_model', 'prompt', 'pdf_to_text', 'resume_store_data', 'generate_ats_score']