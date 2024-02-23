from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////C:\Repositories\flask\dy\maxcode\app\db.py
db = SQLAlchemy(app)

class Truck(db.Model):
    # your code here
    pass
