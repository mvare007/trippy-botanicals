from app import create_app
from app.extensions import db
import pytest


@pytest.fixture()
def app():
    return create_app(test=True)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def _setup_app_context_for_test(app):
    """
    Given app is session-wide, sets up a app context per test to ensure that
    app and request stack is not shared between tests.
    """
    ctx = app.app_context()
    ctx.push()
    yield  # tests will run here
    ctx.pop()


@pytest.fixture()
def database(app):
    """Return a newly initialized database"""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
