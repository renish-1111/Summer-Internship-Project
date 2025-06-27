from models import db

class ResumeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # fields for resume data
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    education = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    certifications = db.Column(db.Text, nullable=True)
    projects = db.Column(db.Text, nullable=True)
    languages = db.Column(db.Text, nullable=True)
    additional_info = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<ResumeData {self.id}>"