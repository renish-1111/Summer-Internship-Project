from Controllers import  prompt
from models import db, ResumeData

def resume_store_data(model, resume_text):
    """
    Process the resume text and return a JSON response with the analysis.
    """
    try:
        response = prompt(model, resume_text, "Analyze this resume and extract key information [name, email, phone, education, experience, skills, certifications, projects, languages, additional_info] in JSON format.")
        if not response:
            return {'error': 'No response from model'}, 400
        print(response)  # Log the response for debugging

        ''' this is response format
   ```json
{
  "name": "Renish Ponkiya",
  "email": "ponkiyarenish@gmail.com",
  "phone": "+91 9687400141",
  "education": [
    {
      "institution": "Government Engineering College Rajkot",
      "degree": "Computer Engineering - BE",
      "dates": "Sep. 2022 – Aug 2026",
      "gpa": "CPI 7.53"
    },
    {
      "institution": "Tapovan Science School",
      "degree": "Higher Secondary-XII",
      "dates": "March. 2021 – May 2022",
      "gpa": "PERCENTAGE 76.67"
    },
    {
      "institution": "Tapovan School",
      "degree": "Secondary-X",
      "dates": "March. 2019 – March 2020",
      "gpa": "PERCENTAGE 78.17"
    }
  ],
  "experience": [],
  "skills": {
    "programming_languages": ["C#", "Python", "Java", "Typescript"],
    "frameworks": [".NET Core", "Flask", "Node.js"],
    "front_end_technologies": ["HTML", "CSS", "JavaScript", "React", "Tailwind CSS", "Bootstrap"],
    "developer_tools": ["Visual Studio Code", "Visual Studio", "GitHub"],
    "databases": ["MySQL", "SQL Server", "MongoDB"]
  },
  "certifications": [],
  "projects": [
    {
      "name": "Auth API",
      "description": "Developed a secure authentication API using .NET Core, SQL Server, and ASP.NET Core Identity. Features include user registration, login, JWT-based token authentication, password hashing, email confirmation, and password reset. The API is fully documented and tested using Swagger UI for easy exploration and testing of endpoints.",
      "technologies": [".NET Core", "SQL Server", "ASP.NET Core Identity", "Swagger UI"]
    },
    {
      "name": "Learning Platform",
      "description": "A web-based platform built with React and Flask to manage and access educational content. Features a responsive UI, real-time updates, and easy sharing of learning resources like videos and notes.",
      "technologies": ["React", "Flask"]
    },
    {
      "name": "GTU Paper Downloader",
      "description": "A web-based tool that allows users to easily search and download GTU exam papers. Built using Flask with a clean and responsive UI powered by HTML and Bootstrap. The app provides quick access to previous papers categorized by subject, semester, and year.",
      "technologies": ["Flask", "HTML", "Bootstrap"]
    },
    {
      "name": "Trip Expense Tracker",
      "description": "A web-based application to help users manage and track their travel expenses efficiently. Built with Flask for the backend, and a responsive frontend using HTML and Bootstrap. Users can add, categorize, and monitor expenses for trips, view summaries, and generate reports to stay within budget.",
      "technologies": ["Flask", "HTML", "Bootstrap", "MYSQL"]
    }
  ],
  "languages": [],
  "additional_info": "Strong interest in .NET and Python development.  Eager to begin my career in a dynamic and innovative organization."
}
```'''
        
        # issue
        # Convert the response to a dictionary if it's a JSON string
        if isinstance(response, str):
            import json
            response = json.loads(response)
        
        resume_data = ResumeData(
            name=response.get('name'),
            email=response.get('email'),
            phone=response.get('phone'),
            education=str(response.get('education')),
            experience=str(response.get('experience')),
            skills=str(response.get('skills')),
            certifications=str(response.get('certifications')),
            projects=str(response.get('projects')),
            languages=str(response.get('languages')),
            additional_info=response.get('additional_info')
        )

        db.session.add(resume_data)
        db.session.commit()
        return {'message': 'Resume data stored successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 400