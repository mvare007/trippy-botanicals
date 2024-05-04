from app import create_app, db
from config import TestingConfig
import pytest

# pytest_plugins = ("pytest-cov", "pytest-azurepipelines")

@pytest.fixture()
def app():
    app = setup()
    yield app
    teardown()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def setup():
    app = create_app()
    testing_config = TestingConfig()
    app.config.from_object(testing_config)
    db.create_all()

    return app

def teardown():
    db.session.remove()
    db.drop_all()

# class AuthActions(object):
#     def __init__(self, client: FlaskClient):
#         self._client = client

#     def login(self, username="test", password="test"):
#         return self._client.post(
#             "/auth/login", data={"username": username, "password": password}
#         )

#     def logout(self):
#         return self._client.get("/auth/logout")