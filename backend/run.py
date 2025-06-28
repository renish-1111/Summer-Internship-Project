import os
import logging
import sys
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log', mode='a')
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main application entry point with error handling"""
    try:
        logger.info("Starting Flask application...")
        
        # Create Flask app
        app = create_app()
        
        if not app:
            logger.error("Failed to create Flask application")
            sys.exit(1)
        
        # Get configuration from environment
        debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        host = os.getenv('FLASK_HOST', '127.0.0.1')
        port = int(os.getenv('FLASK_PORT', 5000))
        
        logger.info(f"Starting server on {host}:{port} (debug={debug_mode})")
        
        # Run the application
        app.run(
            debug=debug_mode,
            host=host,
            port=port,
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
