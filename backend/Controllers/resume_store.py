from Controllers import prompt
from models import db, ResumeData
import json
from validation import (
    clean_json_response,
    extract_basic_info_fallback,
    is_valid_email,
    is_valid_phone
)

def resume_store_data(model, resume_text):
    """
    Process the resume text and return a JSON response with the analysis.
    """
    try:
        # Improved prompt for better JSON response
        prompt_text = f"""
Analyze the following resume text and extract key information. Return ONLY a valid JSON object with these fields:
{{
    "name": "full name of the person",
    "email": "email address",
    "phone": "phone number",
    "education": "education details",
    "experience": "work experience",
    "skills": "technical skills",
    "certifications": "certifications if any",
    "projects": "projects if any",
    "languages": "programming languages or spoken languages",
    "additional_info": "any other relevant information"
}}

Resume text:
{resume_text}

Return only the JSON object, no additional text or explanation.
"""
        
        response = prompt(model, prompt_text)
        if not response:
            return {'error': 'No response from model'}, 400
        
        print("Raw response:", response)  # Log the raw response for debugging
        
        # Clean and parse the response
        cleaned_response = clean_json_response(response)
        print("Cleaned response:", cleaned_response)  # Log cleaned response
        
        # Parse JSON
        try:
            if isinstance(cleaned_response, str):
                data = json.loads(cleaned_response)
            else:
                data = cleaned_response
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            # Fallback: try to extract basic info using regex
            data = extract_basic_info_fallback(response)
        
        # Extract and clean the data
        name = data.get('name', '').strip() if data.get('name') else None
        email = data.get('email', '').strip() if data.get('email') else None
        phone = data.get('phone', '').strip() if data.get('phone') else None
        education = data.get('education', '').strip() if data.get('education') else None
        experience = data.get('experience', '').strip() if data.get('experience') else None
        skills = data.get('skills', '').strip() if data.get('skills') else None
        certifications = data.get('certifications', '').strip() if data.get('certifications') else None
        projects = data.get('projects', '').strip() if data.get('projects') else None
        languages = data.get('languages', '').strip() if data.get('languages') else None
        additional_info = data.get('additional_info', '').strip() if data.get('additional_info') else None

        # Validate extracted data
        if email and not is_valid_email(email):
            email = None
        if phone and not is_valid_phone(phone):
            phone = None
        # if email already in db than update else add
        existing_resume = ResumeData.query.filter_by(email=email).first()
        
        if existing_resume:
            existing_resume.name = name
            existing_resume.phone = phone
            existing_resume.education = education
            existing_resume.experience = experience
            existing_resume.skills = skills
            existing_resume.certifications = certifications
            existing_resume.projects = projects
            existing_resume.languages = languages
            existing_resume.additional_info = additional_info
        else:
            # Create new resume entry
            new_resume = ResumeData(
                name=name,
                email=email,
                phone=phone,
                education=education,
                experience=experience,
                skills=skills,
                certifications=certifications,
                projects=projects,
                languages=languages,
                additional_info=additional_info
            )

        # Save to database
        if existing_resume:
            db.session.add(existing_resume)
            message = "Resume data updated successfully"
        else:
            db.session.add(new_resume)
            message = "Resume data stored successfully"

        db.session.commit()
        
        return {
              'message': message,
              'data': {
                  'name': name,
                  'email': email,
                  'phone': phone,
                  'education': education,
                  'experience': experience,
                  'skills': skills,
                  'certifications': certifications,
                  'projects': projects,
                  'languages': languages,
                  'additional_info': additional_info
              }
        }, 200
        
        
    except Exception as e:
        print(f"Error in resume_store_data: {str(e)}")
        db.session.rollback()  # Rollback in case of error
        return {'error': str(e)}, 400

