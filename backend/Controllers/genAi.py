import os
import logging
import google.generativeai as genai

# Configure logging
logger = logging.getLogger(__name__)

def load_gemini_model():
    """
    Load and configure Gemini model with comprehensive error handling
    """
    try:
        # Check if API key is available
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable not found")
            return None
        
        # Configure Gemini API
        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            return None
        
        # Initialize model
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            # Test the model with a simple prompt
            try:
                test_response = model.generate_content("Hello")
                if not test_response or not test_response.text:
                    logger.warning("Gemini model test returned empty response")
            except Exception as e:
                logger.warning(f"Gemini model test failed (model may still work): {e}")
            
            return model
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            return None
        
    except Exception as e:
        logger.error(f"Unexpected error in load_gemini_model: {e}")
        return None

def prompt(model, *args):
    """
    Generate content using Gemini model with error handling
    """
    try:
        if not model:
            logger.error("Model is None in prompt function")
            return None
        
        # Combine all prompt arguments
        combine_prompt = ""
        for prompt_arg in args:
            if prompt_arg:
                combine_prompt += prompt_arg.strip() + "\n"
        
        if not combine_prompt.strip():
            logger.error("Empty prompt provided")
            return None
        
        # Generate content with error handling
        try:
            response = model.generate_content(combine_prompt.strip())
            
            if not response:
                logger.error("No response received from model")
                return None
            
            if not hasattr(response, 'text') or not response.text:
                logger.error("Response has no text content")
                return None
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Unexpected error in prompt function: {e}")
        return None