from app import db
from .models import *

def create_db():
    db.create_all()