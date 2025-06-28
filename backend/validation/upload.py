import logging

# Configure logging
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """
    Check if uploaded file has allowed extension with error handling
    """
    try:
        if not filename:
            logger.warning("Empty filename provided to allowed_file")
            return False
        
        if not isinstance(filename, str):
            logger.warning(f"Invalid filename type: {type(filename)}")
            return False
        
        # Check if filename contains a dot and has valid extension
        if '.' not in filename:
            logger.warning(f"Filename has no extension: {filename}")
            return False
        
        extension = filename.rsplit('.', 1)[1].lower()
        is_allowed = extension in ALLOWED_EXTENSIONS
        
        return is_allowed
        
    except Exception as e:
        logger.error(f"Error in allowed_file validation: {e}")
        return False
