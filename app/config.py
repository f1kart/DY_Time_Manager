import os

class Config:
    SECRET_KEY = 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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://dyman:Kamber33@localhost:5432/dy_time
    SQLALCHEMY_TRACK_MODIFICATIONS = False