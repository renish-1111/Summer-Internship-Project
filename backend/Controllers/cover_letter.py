from Controllers import prompt

def generate_cover_letter(model, job_description: str, resume_text: str,company_name: str, hiring_manager_name: str,desired_tone: str) -> str:
    """
    Generate a cover letter using the AI model.
    """
    print(company_name)
    print(hiring_manager_name)
    print(desired_tone)

    prompt_text = f"""
You are an expert career coach and a highly skilled copywriter specializing in creating compelling job application materials. Your task is to write a personalized and impactful cover letter based on the provided resume details, job description, and additional user preferences.

**Goal:** Produce a cover letter that effectively highlights the candidate's most relevant skills and experiences, demonstrates a strong understanding of the role and company, and persuades the hiring manager to consider them for an interview.

**Tone:** The cover letter should be professional, confident, enthusiastic, and tailored to resonate with modern hiring practices. It should be concise and focused on value proposition.

---

**User Input:**

1.  resume text (use for fill name, phone, email, link and for extracting relevant skills and experiences):
    {resume_text}

2.  **Job Description:**
    {job_description}

3. **Company Name:**
    {company_name}

4.  **Hiring Manager's Name (Optional):**
    {hiring_manager_name if hiring_manager_name else ''}

5.  **Desired Tone:**
    {desired_tone if desired_tone else 'Standard professional'}

---

**Instructions for LLM:**

* **Extract Contact Information:** From the provided resume text, identify and extract the **candidate's full name, phone number, email address, and any professional links (e.g., LinkedIn profile URL, portfolio URL).** These must be used in the cover letter header.
* **Analyze and Synthesize:** Carefully read both the resume and the job description to identify the most relevant connections between the candidate's qualifications and the job requirements.
* **Tailor Rigorously:** Ensure every paragraph of the cover letter is explicitly tailored to the job description. Avoid generic statements.
* **Highlight Value:** Focus on what the candidate can *do* for the company, not just what they've done. Use action verbs and quantifiable achievements where possible.
* **Structure:**
    * **Cover Letter Header:** Start the letter with the **extracted candidate's full name, phone number, email, and links** (each on a new line or clearly separated). Follow with the current date, then the hiring manager's name (if provided) and company name/address.
    * **Paragraph 1 (Introduction):** Clearly state the position being applied for, where it was seen, and a concise hook about why the candidate is a strong fit (1-2 sentences).
    * **Paragraph 2-3 (Body - Skills & Experience):** Connect the candidate's most relevant skills, experiences, and achievements from the resume to the key requirements of the job description. Use specific examples.
    * **Paragraph 4 (Why Them/Us):** Explain the candidate's genuine interest in the company and/or role. Show cultural fit and enthusiasm.
    * **Paragraph 5 (Call to Action/Closing):** Reiterate enthusiasm, express eagerness for an interview, and thank the reader for their time and consideration.
* **Formatting:** Maintain a professional letter format. Use standard business English.
* **Conciseness:** Keep the letter to a single page, ideally 3-5 paragraphs.
* **Proofread:** Ensure there are no grammatical errors, typos, or awkward phrasing.
"""
    response = prompt(model, prompt_text)
    print(f"Generated cover letter: {response}")
    return response