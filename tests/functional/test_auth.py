import pytest
from app.models.user import User
from factories import UserFactory


def test_login_post(client, database):
    """
    GIVEN a Flask application
    WHEN a POST request is made to the '/login' route
    THEN check that the response is valid and the user is redirected to the index page
    """
    user = UserFactory.create()
    user.set_password("password")
    database.session.add(user)
    database.session.commit()

    data = dict(email=user.email, password="password")
    response = client.post("/login", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/index"


def test_failed_login_post(client, database):
    """
    GIVEN a Flask application
    WHEN a POST request is made to the '/login' route with invalid credentials
    THEN check that the response is valid and the user is redirected to the login page
    """
    response = client.post(
        "/login", data=dict(email="invalid@email.com", password="password")
    )
    redirect_location = response.headers.get("Location")

    assert response.status_code == 302
    assert redirect_location == "/login"


def test_login_get(client, database):
    """
    GIVEN a Flask application
    WHEN a GET request is made to the '/login' route
    THEN check that the response is valid
    """
    response = client.get("/login")

    assert response.status_code == 200


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
    THEN check that the response is valid
    AND the user is created AND the user is redirected to the login page
    """
    email = "test@demo.com"
    response = client.post(
        "/register",
        data=dict(
            {
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
            }
        ),
    )
    user = User.query.filter_by(email=email).first()
    redirect_location = response.headers.get("Location")

    assert response.status_code == 302
    assert redirect_location == "/login"
    assert user is not None

    def test_register_get(client, database):
        """
        GIVEN a Flask application
        WHEN a GET request is made to the '/register' route
        THEN check that the response is valid
        """
        response = client.get("/register")

        assert response.status_code == 200
