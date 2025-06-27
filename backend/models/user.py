import enum
from models import db

class UserRole(enum.Enum):
    USER = 'user'
    ADMIN = 'admin'
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"
