# Routes package initialization
from .api_routes import api_bp
from .pdf_routes import pdf_bp
from .auth_routes import auth_bp

# Export blueprints for easy import
__all__ = ['api_bp', 'pdf_bp','auth_bp']


