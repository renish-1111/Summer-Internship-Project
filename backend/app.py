import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from flask_migrate import Migrate
from models import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

migrate = Migrate()

def create_app():
    """Create and configure Flask application"""
    try:
        # Create Flask application instance
        app = Flask(__name__)
        
        # Load environment variables from .env file first
        load_dotenv()
        
        # Load configuration from Config class for Database
        try:
            app.config.from_object(Config)
            db.init_app(app)
            migrate.init_app(app, db)
            logger.info("Database configuration loaded successfully")
        except Exception as e:
            logger.error(f"Database configuration failed: {e}")
            raise
        
        # Configure CORS - allow requests from frontend
        try:
            urls = os.getenv("FRONTEND_URL")
            urls = urls.split(",") if urls else []
            CORS(app, resources={r"/api/*": {"origins": urls}})
            logger.info(f"CORS configured for frontend URLs: {urls}")
        except Exception as e:
            logger.error(f"CORS configuration failed: {e}")
            raise
        
        # Setup upload folder
        try:
            UPLOAD_FOLDER = 'uploads'  # Directory to save uploaded PDFs
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists
            logger.info(f"Upload folder configured: {UPLOAD_FOLDER}")
        except Exception as e:
            logger.error(f"Upload folder setup failed: {e}")
            raise
        
        # Import and register blueprints
        try:
            from routes import api_bp, pdf_bp
            @app.route('/check')
            def check():
                return jsonify({"status": "ok"})
            app.register_blueprint(api_bp, url_prefix='/api')
            app.register_blueprint(pdf_bp, url_prefix='/api')
            logger.info("Blueprints registered successfully")
        except ImportError as e:
            logger.error(f"Blueprint import failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Blueprint registration failed: {e}")
            raise

        # Add global error handlers
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({
                'success': False,
                'error': 'Resource not found',
                'message': 'The requested resource was not found'
            }), 404
        
        @app.errorhandler(500)
        def internal_error(error):
            logger.error(f"Internal server error: {error}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'message': 'An internal error occurred'
            }), 500
        
        # Create database tables
        try:
            with app.app_context():
                db.create_all()
                logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Database table creation failed: {e}")
            # Don't raise here as app can still function without tables initially

        logger.info("Flask application created successfully")
        return app
        
    except Exception as e:
        logger.error(f"Flask application creation failed: {e}")
        raise


