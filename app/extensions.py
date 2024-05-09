from flask_admin import Admin
from app.admin.custom_views import AdminModelView, DashboardView
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Bootstrap - https://bootstrap-flask.readthedocs.io
bootstrap = Bootstrap5()

# Flask SQL Alchemy - https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
db = SQLAlchemy()

# Flask Migrate - https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate()

# Flask Login - https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."

# Flask Admin - https://flask-admin.readthedocs.io/en/latest/
def register_flask_admin(app, db, models):
		admin = Admin(app, name="Trippy Botanicals", template_mode="bootstrap4", index_view=DashboardView())
		for model in models:
				admin.add_view(AdminModelView(model, db.session))
