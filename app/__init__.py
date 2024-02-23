from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dyconcrete.db'  # or 'postgresql://user:password@localhost/dyconcrete' for production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from app.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from app.tech import tech as tech_blueprint
app.register_blueprint(tech_blueprint, url_prefix='/tech')

from app import routes

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)), models


