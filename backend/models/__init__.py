from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models so Flask-Migrate detects them
from .resume_data import ResumeData

__all__ = ['db', 'ResumeData']
