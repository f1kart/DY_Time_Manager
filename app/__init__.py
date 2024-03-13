from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dyconcrete.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from app.auth.routes import auth_bp
from app.routes import main_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

from app.models import User, Truck

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    
    # rest of your create_app function...
    
    return app