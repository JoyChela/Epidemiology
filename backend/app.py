from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
app = Flask(__name__)

# Configure your database URI (example for SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epidemiology.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration tool
db.init_app(app)
migrate = Migrate(app, db)
