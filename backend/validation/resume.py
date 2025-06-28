import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

def clean_json_response(response):
    """
    Clean the AI response to extract valid JSON with error handling
    """
    try:
        if not response:
            logger.warning("Empty response provided to clean_json_response")
            return ""
        
        if not isinstance(response, str):
            return response
        
        # Remove markdown code blocks if present
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*$', '', response)
        
        # Find JSON object in the response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            cleaned = json_match.group(0)
            return cleaned
        
        logger.warning("No JSON object found in response")
        return response
        
    except Exception as e:
        logger.error(f"Error in clean_json_response: {e}")
        return response

def extract_basic_info_fallback(text):
    """
    Fallback method to extract basic info using regex if JSON parsing fails
    """
    try:
        if not text:
            logger.warning("Empty text provided to extract_basic_info_fallback")
            return {}
        
        data = {}
        
        # Extract email
        try:
            email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
            if email_match:
                data['email'] = email_match.group(0)
        except Exception as e:
            logger.warning(f"Email extraction failed: {e}")
        
        # Extract phone (various formats)
        try:
            phone_patterns = [
                r'(\+\d{1,3}[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',
                r'(\+\d{1,3}[-.\s]?)?\d{10}',
                r'(\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
            ]
            
            for pattern in phone_patterns:
                phone_match = re.search(pattern, text)
                if phone_match:
                    data['phone'] = phone_match.group(0)
                    break
        except Exception as e:
            logger.warning(f"Phone extraction failed: {e}")
        
        # Try to extract name (basic attempt)
        try:
            lines = text.split('\n')
            for line in lines[:5]:  # Check first 5 lines
                line = line.strip()
                if len(line) > 3 and len(line) < 50 and ' ' in line:
                    # Basic name detection (contains space, reasonable length)
                    if not any(char.isdigit() for char in line) and '@' not in line:
                        data['name'] = line
                        break
        except Exception as e:
            logger.warning(f"Name extraction failed: {e}")
        
        return data
        
    except Exception as e:
        logger.error(f"Error in extract_basic_info_fallback: {e}")
        return {}

def is_valid_email(email):
    """
    Basic email validation with error handling
    """
    try:
        if not email:
            return False
        
        if not isinstance(email, str):
            logger.warning(f"Email is not a string: {type(email)}")
            return False
        
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        is_valid = re.match(pattern, email) is not None
        
        return is_valid
        
    except Exception as e:
        logger.error(f"Error in email validation: {e}")
        return False

def is_valid_phone(phone):
    """
    Basic phone validation with error handling
    """
    try:
        if not phone:
            return False
        
        if not isinstance(phone, str):
            logger.warning(f"Phone is not a string: {type(phone)}")
            return False
        
        # Remove all non-digit characters and check length
        digits_only = re.sub(r'\D', '', phone)
        is_valid = len(digits_only) >= 10
        
        return is_valid
        
    except Exception as e:
        logger.error(f"Error in phone validation: {e}")
        return False