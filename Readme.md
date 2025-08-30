## Summer Internship Project

This project is a full-stack web application consisting of a frontend (likely built with a modern JS framework) and a Python backend (Flask), orchestrated using Docker Compose. It is designed to process resumes, generate cover letters, and provide AI-powered features.

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
3. The frontend will be available at [http://localhost](http://localhost) and the backend API at [http://localhost:5000](http://localhost:5000).

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


---

## Tech Stack

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

- **Resume Upload & Analysis:**  
    `POST /api/pdf-analysis`  
    Upload a PDF resume and receive an AI-powered analysis, including feedback and improvement suggestions.

- **Cover Letter Generation:**  
    `POST /api/cover_letter`  
    Generate a tailored cover letter using your resume text and a job description.

- **ATS Optimization:**  
    `POST /api/ats`  
    Analyze your resume for Applicant Tracking System (ATS) compatibility and receive an ATS score.

- **PDF Data Extraction:**  
    Extract and process text from uploaded PDF resumes.

- **Health Check:**  
    `GET /api/health`  
    Check backend service and AI model status.

See `backend/routes/` and `backend/Controllers/` for detailed endpoint implementations and logic.

---

## Page Overview

### Frontend Pages
- **Home**: Landing page/introduction
- **Resume Upload**: Upload and manage resumes (PDF)
- **Cover Letter Generator**: Generate cover letters using AI
- **ATS Analysis**: Analyze resumes for ATS compatibility

---

For more details, see the code in each subfolder or contact the project maintainer.
