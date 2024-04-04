from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()
db.init_app(app)

if __name__ == "__main__":
	# We need to make sure Flask knows about its views before we run
	# the app, so we import them. We could do it earlier, but there's
	# a risk that we may run into circular dependencies, so we do it at the
	# last minute here.

	from views import *

	app.run(debug=True)

