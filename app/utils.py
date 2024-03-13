from datetime import datetime
from flask import current_app

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints 
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.main import main_bp
    app.register_blueprint(main_bp)

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format)

    # ... other blueprints

    return app
