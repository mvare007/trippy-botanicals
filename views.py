from flask import render_template, request
from app import app
from models import *

@app.route('/')
def index():
	return 'Teste'
