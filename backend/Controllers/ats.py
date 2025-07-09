from Controllers import prompt
import json

def generate_ats_score(model, resume_text: str, job_description : str) -> float or None:
    """
    Generate an ATS (Applicant Tracking System) score for a resume given a job description using the provided AI model.
    Returns a score (float or int) or None if generation fails.
    """
    if not model or not resume_text:
        return None

    # Compose the prompt for the AI model
    ats_prompt = f"""
You are an expert ATS (Applicant Tracking System) simulator and recruitment analyst. Evaluate the given resume projects,skills,education,experience,work,keyword against the job description and return an **ATS Match Score** with brief justification.

**Goal:** Help the candidate optimize their resume to increase its chances of passing ATS filters and appealing to recruiters.

**Input:**
1. **Resume Text:** {resume_text}
2. **Job Description:** {job_description}

**Output Format:** 
```json
"ats_score": 85
```
"""

    try:
        # Call the model (assume OpenAI-like interface)
        response = prompt(model, ats_prompt)
        print(type(response))  # Ensure the response is in the expected format
        print(f"Generated ATS score response: {response}")
        import re
        match = re.search(r'"?ats_score"?\s*:\s*(\d+)', str(response))
        if match:
            ats_score = float(match.group(1))
            print(f"Parsed ATS score: {ats_score}")
            return ats_score
        else:
            print("Could not find ats_score in response")
            return None
        
    except Exception as e:
        # Optionally log error here if logger is available
        print(f"Error generating ATS score: {e}")
        return None
