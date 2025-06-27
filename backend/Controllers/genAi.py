import os
import google.generativeai as genai

def load_gemini_model():
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        return model
        
    except Exception as e:
        print(f"Error initializing Gemini model: {e}")
        model = None
        return model

def prompt(model,*args):
    combine_prompt = ""
    for prompt in args:
        if prompt:
            combine_prompt += prompt.strip() + "\n"
    if combine_prompt:
        response =  model.generate_content(combine_prompt.strip())
        return response.text
    else:
        return None