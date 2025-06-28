import logging
import json
import datetime
from Controllers import prompt
from models import db, ResumeData
from validation import (
    clean_json_response,
    extract_basic_info_fallback,
    is_valid_email,
    is_valid_phone
)

# Configure logging
logger = logging.getLogger(__name__)

def log_error(error_type, error_message, context=""):
    """Utility function for consistent error logging"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {error_type}: {error_message}"
    if context:
        log_message += f" | Context: {context}"
    logger.error(log_message)

def resume_store_data(model, resume_text):
    """
    Process the resume text and store in database with comprehensive error handling
    """
    try:
        # Input validation
        if not model:
            log_error("ModelError", "Model is None", "resume_store_data")
            return {'error': 'AI model not available'}, 503
        
        if not resume_text or not resume_text.strip():
            log_error("InputError", "Resume text is empty", "resume_store_data")
            return {'error': 'Resume text is required'}, 400
        
        # Truncate very long resume text to prevent API limits
        max_text_length = 10000  # Adjust based on your API limits
        if len(resume_text) > max_text_length:
            resume_text = resume_text[:max_text_length]
            logger.warning(f"Resume text truncated to {max_text_length} characters")
        
        # Generate AI prompt for data extraction
        try:
            prompt_text = f"""
Analyze the following resume text and extract key information. Return ONLY a valid JSON object with these fields:
{{
    "name": "full name of the person",
    "email": "email address",
    "phone": "phone number",
    "education": "education details",
    "experience": "work experience",
    "skills": "technical skills and framework language",
    "certifications": "certifications if any",
    "projects": "projects if any",
    "languages": "spoken languages",
    "additional_info": "any other relevant information"
}}

Resume text:
{resume_text}

Return only the JSON object, no additional text or explanation.
"""
            
            logger.info("Generating AI response for resume data extraction")
            response = prompt(model, prompt_text)
            
            if not response:
                log_error("AIResponseError", "No response from model", "resume_store_data")
                return {'error': 'Failed to process resume with AI'}, 500
            
            logger.info(f"Raw AI response length: {len(response)}")
            
        except Exception as e:
            log_error("AIProcessingError", str(e), "resume_store_data")
            return {'error': 'AI processing failed'}, 500
        
        # Clean and parse the AI response
        try:
            cleaned_response = clean_json_response(response)
            logger.info("Response cleaned successfully")
            
            # Parse JSON
            if isinstance(cleaned_response, str):
                data = json.loads(cleaned_response)
            else:
                data = cleaned_response
                
            logger.info("JSON parsing successful")
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed: {e}, attempting fallback extraction")
            # Fallback: try to extract basic info using regex
            try:
                data = extract_basic_info_fallback(response)
                if not data:
                    log_error("FallbackExtractionError", "Fallback extraction returned empty data", "resume_store_data")
                    return {'error': 'Failed to extract data from resume'}, 500
                logger.info("Fallback extraction successful")
            except Exception as fallback_error:
                log_error("FallbackExtractionError", str(fallback_error), "resume_store_data")
                return {'error': 'Data extraction failed'}, 500
        except Exception as e:
            log_error("DataProcessingError", str(e), "resume_store_data")
            return {'error': 'Data processing failed'}, 500
        
        # Extract and validate data
        try:
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
                logger.warning(f"Invalid email format: {email}")
                email = None
            if phone and not is_valid_phone(phone):
                logger.warning(f"Invalid phone format: {phone}")
                phone = None
                
            # Generate anonymous name if missing
            if not name:
                name = f"Anonymous_User_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                logger.info(f"Generated anonymous name: {name}")
            
            logger.info(f"Data extracted - Name: {name}, Email: {email}")
            
        except Exception as e:
            log_error("DataValidationError", str(e), "resume_store_data")
            return {'error': 'Data validation failed'}, 500
        
        # Database operations
        try:
            existing_resume = None
            if email:
                existing_resume = ResumeData.query.filter_by(email=email).first()
            
            if existing_resume:
                # Update existing record
                try:
                    existing_resume.name = name
                    existing_resume.phone = phone
                    existing_resume.education = education
                    existing_resume.experience = experience
                    existing_resume.skills = skills
                    existing_resume.certifications = certifications
                    existing_resume.projects = projects
                    existing_resume.languages = languages
                    existing_resume.additional_info = additional_info
                    existing_resume.updated_at = datetime.datetime.utcnow()
                    
                    db.session.commit()
                    message = "Resume data updated successfully"
                    logger.info(f"Updated existing resume for email: {email}")
                    
                except Exception as e:
                    db.session.rollback()
                    log_error("DatabaseUpdateError", str(e), f"Email: {email}")
                    return {'error': 'Failed to update resume data'}, 500
            else:
                # Create new record
                try:
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
                    
                    db.session.add(new_resume)
                    db.session.commit()
                    message = "Resume data stored successfully"
                    logger.info(f"Created new resume record for: {name}")
                    
                except Exception as e:
                    db.session.rollback()
                    log_error("DatabaseInsertError", str(e), f"Name: {name}")
                    return {'error': 'Failed to store resume data'}, 500
            
            # Return success response
            return {
                'success': True,
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
                },
                'timestamp': datetime.datetime.now().isoformat()
            }, 200
            
        except Exception as e:
            try:
                db.session.rollback()
            except:
                pass
            log_error("DatabaseError", str(e), "resume_store_data")
            return {'error': 'Database operation failed'}, 500
        
    except Exception as e:
        # Handle any unexpected errors
        try:
            db.session.rollback()
        except:
            pass
        log_error("UnexpectedError", str(e), "resume_store_data")
        return {'error': 'An unexpected error occurred'}, 500

