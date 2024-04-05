from app import db
from .user import User

def create_db():
    db.create_all()