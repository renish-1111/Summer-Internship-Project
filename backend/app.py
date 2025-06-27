import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from flask_migrate import Migrate
from models import db

migrate = Migrate()

def create_app():
    # Create Flask application instance
    app = Flask(__name__)
    
    # Load configuration from Config class for Database
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Configure CORS - allow requests from frontend
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    CORS(app, resources={r"/api/*": {"origins": [frontend_url]}})
    
    UPLOAD_FOLDER = 'uploads'  # Directory to save uploaded PDFs
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists
    
    # Import blueprints
    from routes import api_bp, pdf_bp, auth_bp
    # Register blueprints with URL prefix
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(pdf_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app


