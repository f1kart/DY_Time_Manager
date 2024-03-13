from your_application import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db = SQLAlchemy(app)

# Define your models here
class dymodelodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # other fields

# Create the tables
with app.app_context():
    db.create_all()
