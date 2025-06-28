import os
import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

try:
    from validation import allowed_file
    from Controllers import pdf_to_text, load_gemini_model, prompt, resume_store_data
    from models import db, ResumeData
except ImportError as e:
    print(f"Import error: {e}")
    raise

# Create blueprint for PDF analysis routes
pdf_bp = Blueprint('pdf', __name__)

# Load model once when the blueprint is imported
try:
    model = load_gemini_model()
    if not model:
        print("Warning: Gemini model not initialized")
except Exception as e:
    print(f"Error loading Gemini model: {e}")
    model = None

def log_error(error_type, error_message, context=""):
    """
    Utility function for consistent error logging
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {error_type}: {error_message}"
    if context:
        log_message += f" | Context: {context}"
    print(log_message)

@pdf_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify service status
    """
    try:
        status = {
            'success': True,
            'status': 'healthy',
            'model_available': model is not None,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        if not model:
            status['success'] = False
            status['status'] = 'degraded'
            status['warning'] = 'AI model not available'
            
        return jsonify(status), 200 if model else 503
        
    except Exception as e:
        log_error("HealthCheck", str(e))
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': 'Health check failed'
        }), 500

@pdf_bp.route('/pdf-analysis', methods=['POST'])
def upload_pdf():
    try:
        # Check if model is available
        if not model:
            return jsonify({
                'success': False,
                'error': 'AI service temporarily unavailable',
                'message': 'Please try again later'
            }), 503
            
        if 'pdfFile' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided',
                'message': 'No file part in the request'
            }), 400

        file = request.files['pdfFile']

        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected',
                'message': 'No selected file'
            }), 400

        if file and allowed_file(file.filename):
            try: 
                # file name + time stamp to avoid conflicts
                filename = secure_filename(file.filename)
                filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                
                # Get upload folder from app config
                upload_folder = current_app.config['UPLOAD_FOLDER']
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)

                # Process the PDF file
                try:
                    extracted_text = pdf_to_text(file_path)
                    
                    if not extracted_text:
                        return jsonify({
                            'success': False,
                            'error': 'Text extraction failed',
                            'message': 'Failed to extract text from PDF'
                        }), 400
                except Exception as e:
                    log_error("PDFExtraction", str(e), f"File: {filename}")
                    return jsonify({
                        'success': False,
                        'error': 'PDF processing failed',
                        'message': 'Error processing PDF file'
                    }), 500
                
                try:
                    job_description = request.form.get('jobDescription', 'Software Engineer')
                    
                    prompt_text = f"""
You are an advanced career coach and AI resume expert. Please analyze the resume content provided below and deliver structured, in-depth feedback based on the following dimensions. Your goal is to help improve this resume's effectiveness, clarity, and alignment with industry standards and job expectations.

---

✅ Evaluation Criteria:

1. Structure & Readability
– Is the resume well-organized with logical flow? Are section headings clear and consistent?

2. Professional Summary
– Does it effectively communicate the candidate's career goals, value proposition, and core strengths in 2–4 sentences?

3. Skills Relevance
– Are the skills listed relevant to the candidate's industry or target role? Are there any missing in-demand skills?

4. Work Experience Impact
– Are achievements action-oriented and quantified where possible? Do they demonstrate progression, leadership, or business value?

5. ATS Optimization
– Does the resume use keywords likely to pass through an Applicant Tracking System (ATS)? Highlight any key terms that should be added.

6. Grammar, Style & Tone
– Point out any grammar, spelling, or tone inconsistencies. Suggest ways to enhance professionalism.

7. Visual Formatting
– Is the layout clean, scannable, and aligned with modern resume standards? Are fonts, bullet points, and white space appropriately used?

8. Tailoring to Job Description (Optional)
– If a job description is provided below, assess how well the resume aligns with it. Suggest key customizations.

---

📄 Resume Text:
{extracted_text}

📌 (Optional) Target Job Description:
{job_description}

---

🔚 Output Format:

- Strengths Summary
- Section-by-Section Analysis
- ATS Readiness Score (/100)
- Improvement Recommendations
- Rewritten Bullet Examples (if applicable)
- Final Verdict: Ready / Needs Work / Major Revision

Please respond with your full analysis and without any additional text or explanations.

NOTE: If user not provided resume pdf then just response with this "No resume provided for analysis. Please upload a valid PDF resume."
"""

                    response = prompt(model, prompt_text)
                    
                    if response == "No resume provided for analysis. Please upload a valid PDF resume.":
                        return jsonify({
                            'success': False,
                            'error': 'No resume provided',
                            'message': response
                        }), 400
                    elif not response:
                        log_error("AIResponse", "Empty response from model", f"File: {filename}")
                        return jsonify({
                            'success': False,
                            'error': 'Analysis generation failed',
                            'message': 'Failed to generate analysis'
                        }), 500
                    
                    # Store resume data in the database
                    try:
                        resume_data_response = resume_store_data(model, extracted_text)
                        print(f"Resume data stored successfully")
                    except Exception as e:
                        log_error("ResumeStorage", str(e), f"File: {filename}")
                        # Continue with analysis even if storage fails

                    # Return successful response
                    return jsonify({
                        'success': True,
                        'message': response,
                        'filename': filename,
                        'metadata': {
                            'text_length': len(extracted_text),
                            'job_description': job_description,
                            'processed_at': datetime.datetime.now().isoformat()
                        }
                    }), 200

                except Exception as e:
                    log_error("AIAnalysis", str(e), f"File: {filename}")
                    return jsonify({
                        'success': False,
                        'error': 'Analysis generation failed',
                        'message': 'Error generating resume analysis'
                    }), 500

            except Exception as e:
                log_error("FileProcessing", str(e), f"File: {file.filename if file else 'unknown'}")
                return jsonify({
                    'success': False,
                    'error': 'File processing failed',
                    'message': 'Error processing uploaded file'
                }), 500
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid file type',
                'message': 'Invalid file type or no file selected'
            }), 400
            
    except Exception as e:
        log_error("UnexpectedError", str(e), "upload_pdf function")
        return jsonify({
            'success': False,
            'error': 'Unexpected error occurred',
            'message': 'An unexpected error occurred'
        }), 500
