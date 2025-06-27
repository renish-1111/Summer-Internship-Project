import re

def clean_json_response(response):
    """
    Clean the AI response to extract valid JSON
    """
    if not isinstance(response, str):
        return response
    
    # Remove markdown code blocks if present
    response = re.sub(r'```json\s*', '', response)
    response = re.sub(r'```\s*$', '', response)
    
    # Find JSON object in the response
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    return response

def extract_basic_info_fallback(text):
    """
    Fallback method to extract basic info using regex if JSON parsing fails
    """
    data = {}
    
    # Extract email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        data['email'] = email_match.group(0)
    
    # Extract phone (various formats)
    phone_match = re.search(r'(\+\d{1,3}[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})', text)
    if phone_match:
        data['phone'] = phone_match.group(0)
    
    # Try to extract name (basic attempt)
    lines = text.split('\n')
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if len(line) > 3 and len(line) < 50 and ' ' in line:
            # Basic name detection (contains space, reasonable length)
            if not any(char.isdigit() for char in line) and not '@' in line:
                data['name'] = line
                break
    
    return data

def is_valid_email(email):
    """
    Basic email validation
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """
    Basic phone validation
    """
    # Remove all non-digit characters and check length
    digits_only = re.sub(r'\D', '', phone)
    return len(digits_only) >= 10