from sqlalchemy import DateTime, func
from models import db

class ResumeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    education = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.String(255), nullable=True)
    skills = db.Column(db.String(255), nullable=True)
    certifications = db.Column(db.String(255), nullable=True)
    projects = db.Column(db.String(255), nullable=True)
    languages = db.Column(db.String(255), nullable=True)
    additional_info = db.Column(db.String(255), nullable=True)
    created_at = db.Column(DateTime, default=func.now())  

    def __repr__(self):
        return f"<ResumeData {self.id} >"