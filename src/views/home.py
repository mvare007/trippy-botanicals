from flask import render_template, request
from app import app


@app.route('/')
def home():
	return render_template('home.html')
