from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    # rest of your model definition...
