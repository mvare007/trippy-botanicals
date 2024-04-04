from app import app, db

class User(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		username = db.Column(db.String(80), unique=True, nullable=False)
		email = db.Column(db.String(120), unique=True, nullable=False)

		def __init__(self, username, email):
			self.username = username
			self.email = email

with app.app_context():
    db.create_all()