from flask_bootstrap import Bootstrap4
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
environment = environ['FLASK_ENV']
bootstrap = Bootstrap4(app) # https://bootstrap-flask.readthedocs.io

# Configuration
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

# Database
db = SQLAlchemy()
db.init_app(app)

# Views
from src.views import *

if __name__ == "__main__":
	app.run()

