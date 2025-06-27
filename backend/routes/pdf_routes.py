import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from validation.upload import allowed_file
from Controllers import pdf_to_text,load_gemini_model, prompt, resume_store_data
from models import db, ResumeData

# Create blueprint for PDF analysis routes
pdf_bp = Blueprint('pdf', __name__)

# Load model once when the blueprint is imported
model = load_gemini_model()

@pdf_bp.route('/pdf-analysis', methods=['POST'])
def upload_pdf():
    if 'pdfFile' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['pdfFile']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Get upload folder from app config
        from flask import current_app
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file.save(os.path.join(upload_folder, filename))

        # Process the PDF file
        pdf_path = os.path.join(upload_folder, filename)
        
        extracted_text = pdf_to_text(pdf_path)
        
        if not extracted_text:
            return jsonify({'message': 'Failed to extract text from PDF'}), 400
        
        # Store resume data in the database
        resume_data_response = resume_store_data(model, extracted_text)
        print(resume_data_response)  # Log the response for debugging
        
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

Please respond with your full analysis.
"""

        response = prompt(model, prompt_text)

        return jsonify({'message': response, 'filename': filename}), 200
    else:
        return jsonify({'message': 'Invalid file type or no file selected'}), 400
