from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models so Flask-Migrate detects them
from .user import User
from .resume_data import ResumeData

__all__ = ['db', 'User', 'ResumeData']
