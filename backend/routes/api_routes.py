import datetime
import logging
from flask import Blueprint, request, jsonify

try:
    from Controllers import load_gemini_model, prompt
except ImportError as e:
    logging.error(f"Import error in api_routes: {e}")
    raise

# Create blueprint for general API routes
api_bp = Blueprint('api', __name__)

# Configure logging
logger = logging.getLogger(__name__)

# Load model once when the blueprint is imported
try:
    model = load_gemini_model()
    if not model:
        logger.warning("Gemini model not initialized in api_routes")
except Exception as e:
    logger.error(f"Error loading Gemini model in api_routes: {e}")
    model = None

def log_error(error_type, error_message, context=""):
    """Utility function for consistent error logging"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {error_type}: {error_message}"
    if context:
        log_message += f" | Context: {context}"
    logger.error(log_message)

@api_bp.route('/health', methods=['GET'])
def api_health_check():
    """API health check endpoint"""
    try:
        status = {
            'success': True,
            'service': 'General API Service',
            'status': 'healthy' if model else 'degraded',
            'model_available': model is not None,
            'timestamp': datetime.datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        if not model:
            status['success'] = False
            status['warnings'] = ['AI model not available']
            
        return jsonify(status), 200 if model else 503
        
    except Exception as e:
        log_error("APIHealthCheck", str(e))
        return jsonify({
            'success': False,
            'service': 'General API Service',
            'status': 'unhealthy',
            'error': 'Health check failed',
            'timestamp': datetime.datetime.now().isoformat()
        }), 500

@api_bp.route('/hello', methods=['GET'])
def hello_world():
    """Simple hello endpoint with AI integration"""
    try:
        if not model:
            return jsonify({
                'success': False,
                'error': 'AI service temporarily unavailable',
                'message': 'Service temporarily unavailable'
            }), 503
            
        if request.method == "GET":
            try:
                # Generate AI response with error handling
                response = prompt(model, "who is prime minister of india?", "Gujarat cm name")
                
                if not response:
                    log_error("EmptyAIResponse", "No response from AI model", "hello endpoint")
                    return jsonify({
                        'success': False,
                        'error': 'Empty response from AI',
                        'message': 'Please try again'
                    }), 500
                
                return jsonify({
                    'success': True,
                    'message': response,
                    'timestamp': datetime.datetime.now().isoformat()
                }), 200
                
            except Exception as e:
                log_error("AIPromptError", str(e), "hello endpoint")
                return jsonify({
                    'success': False,
                    'error': 'AI processing failed',
                    'message': 'Unable to generate response'
                }), 500
        
        return jsonify({
            'success': False,
            'error': 'Method not allowed'
        }), 405
        
    except Exception as e:
        log_error("UnexpectedError", str(e), "hello_world function")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred',
            'message': 'Please try again or contact support'
        }), 500
