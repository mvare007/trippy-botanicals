import pytest
from app.models.user import User

def test_register_get(client, database):
	"""
		GIVEN a Flask application
		WHEN a POST request is made to the '/register' route
		THEN check that the response is valid and the user is created
	"""
	response = client.get("/register")
	assert response.status_code == 200


def test_register_post(client, database):
	"""
		GIVEN a Flask application
		WHEN a POST request is made to the '/register' route
		THEN check that the response is valid and the user is created
	"""
	email = "test@demo.com"
	response = client.post("/register", data=dict({
	"email": email,
	"first_name": "Homer",
	"last_name": "Simpson",
	"address": "123 Main St",
	"zip_code": "1234-999",
	"location": "Springfield",
	"vat_number": "123456789",
	"phone": "1234567890",
	"password": "password",
		"password2": "password",
	}))
	user = User.query.filter_by(email=email).first()

	assert response.status_code == 302
	assert user is not None