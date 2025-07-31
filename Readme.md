
## Summer Internship Project

This project is a full-stack web application for resume and cover letter management, powered by AI. It features:

- **AI Resume Analysis:** Upload your resume (PDF) and receive detailed, actionable feedback.
- **Cover Letter Generation:** Instantly generate tailored cover letters for any job description.
- **ATS Optimization:** Analyze and improve your resume for Applicant Tracking Systems.
- **Modern UI:** Fast, responsive frontend with smooth animations and clean design.
- **Easy Deployment:** One-command Docker Compose setup for local or cloud deployment.

---

---


### Folder Structure

- `backend/` - Python Flask backend API
  - `Controllers/` - Business logic and API controllers
  - `models/` - Database models
  - `routes/` - API route definitions
  - `validation/` - Input validation logic
  - `uploads/` - Uploaded PDF files
  - `instance/` - SQLite database files
  - `migrations/` - Alembic migration scripts
  - `requirements.txt` - Python dependencies
  - `Dockerfile` - Backend Docker build
- `frontend/` - Frontend application (Vite/React or similar)
  - `src/` - Frontend source code
  - `public/` - Static assets
  - `Dockerfile` - Frontend Docker build
- `docker-compose.yml` - Multi-container orchestration

---

### Running the Project


1. **Install Docker & Docker Compose**
2. In the project root, run:
   ```powershell
   docker-compose up --build
   ```
3. Open your browser:
   - Frontend: [http://localhost](http://localhost)
   - Backend API: [http://localhost:5000](http://localhost:5000)

---

### Environment Variables

**Backend:**
- `FRONTEND_URL` - Allowed origins for CORS
- `GEMINI_API_KEY` - API key for AI features
- `DATABASE_URL` - Database connection string (default: SQLite)
- `FLASK_DEBUG` - Flask debug mode

---

### Health Checks

- **Frontend:** `http://localhost/` (returns 200 if healthy)
- **Backend:** `http://localhost:5000/api/health` (returns 200 if healthy)

---

### Data Persistence

The backend uses a Docker volume (`sqlite_data`) to persist the SQLite database between container restarts.

---


### Credits

Developed by Renish Ponkiya and contributors.

---

## Screenshots

<!-- Uncomment and add screenshots or GIFs here -->
<!--
![Home Page](screenshots/home.png)
![Resume Analysis](screenshots/analysis.gif)
-->

---


---


## Tech Stack

### Frontend
- Vite (React)
- TypeScript
- Tailwind CSS
- Framer Motion (animations)
- Nginx (serving static files)

### Backend
- Python 3 (Flask)
- SQLAlchemy (ORM)
- Alembic (migrations)
- Gemini API (AI features)

### DevOps
- Docker & Docker Compose
- Jenkins (CI/CD pipeline)
- Azure Virtual Machine (VM) for deployment

### Other
- SQLite (database)

---


## API Overview

The backend exposes a RESTful API for:

### Resume Upload & Analysis
**POST `/api/pdf-analysis`**
- Upload a PDF resume and receive an AI-powered analysis, including feedback and improvement suggestions.
- **Request:**
#### Example Response

```json
{
    "filename": "resume.pdf",
    "output": "Strengths Summary\nRenish's resume effectively showcases...",
    "metadata": {
        "job_description": "Software Engineer at ExampleCorp",
        "processed_at": "2024-06-10T14:23:45Z",
        "text_length": 2450
    },
    "resume_text": "John Doe\nExperienced software engineer with expertise in Python, Flask, and cloud technologies...",
    "success": true
},200
```

### Cover Letter Generation
**POST `/api/cover_letter`**
- Generate a tailored cover letter using your resume text and a job description.
- **Request:**
  - Form-data: `resume_text` (string)
  - Query params: `job_description`, `company_name`, `hiring_manager_name`, `desired_tone`
- **Response:**
- JSON with generated cover letter, for example:

```json
{
    "success": true,
    "cover_letter": "Dear Hiring Manager,\nI am excited to apply for the Software Engineer position at ExampleCorp...",
    "timestamp": "2024-06-10T15:42:30.123456"
},200
```

### ATS Optimization
**POST `/api/ats`**
- Analyze your resume for ATS compatibility and receive an ATS score.
- **Request:**
  - Form-data: `resume_text` (string), optional `job_description` (string)
- **Response:**
- JSON with ATS score, for example:

```json
{
    "success": true,
    "ats_score": 87,
    "timestamp": "2024-06-10T16:05:12.789012"
},200
```

### Health Check
**GET `/api/health`**
- Check backend service and AI model status.

See `backend/routes/` and `backend/Controllers/` for detailed endpoint implementations and logic.

---


## Page Overview

### Frontend Pages
- **Home:** Landing page/introduction
- **Resume Upload:** Upload and manage resumes (PDF)
- **Cover Letter Generator:** Generate cover letters using AI
- **ATS Analysis:** Analyze resumes for ATS compatibility
- **PDF Data Extraction:** View extracted text and analysis results

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request. For major changes, discuss them first.

---

## License

This project is licensed under the MIT License.

---

For more details, see the code in each subfolder or contact the project maintainer.
