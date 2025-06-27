from flask import Blueprint, request, jsonify
from Controllers import load_gemini_model, prompt

# Create blueprint for general API routes
api_bp = Blueprint('api', __name__)

# Load model once when the blueprint is imported
model = load_gemini_model()

@api_bp.route('/hello', methods=['GET'])
def hello_world():
    if request.method == "GET":
        if model:
            try:
                response = prompt(model, "who is prime minister of india?", "Gujarat cm name")
                return jsonify({'message': response}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'Model not initialized'}), 400
