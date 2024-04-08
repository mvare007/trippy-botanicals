from os import environ
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flask - https://flask.palletsprojects.com
app = Flask(__name__)

# Bootstrap - https://bootstrap-flask.readthedocs.io
bootstrap = Bootstrap5(app)

# Configuration
environment = environ['FLASK_ENV']
if environment == 'production':
	from config import ProductionConfig
	app.config.from_object(ProductionConfig())
elif environment == 'development':
	from config import DevelopmentConfig
	app.config.from_object(DevelopmentConfig())
elif environment == 'test':
	from config import TestingConfig
	app.config.from_object(TestingConfig())
else:
	raise ValueError('Invalid environment name')

# Database - https://sqlalchemy-seeder.readthedocs.io/en/latest/
db = SQLAlchemy()
db.init_app(app)

# Flask Migrate - https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate(app, db)

# Flask Login - https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

with app.app_context():
	from app import routes, models
	# db.create_all()
