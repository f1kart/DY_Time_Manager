import os

class Config:
    SECRET_KEY = os.environ.get('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') or 'you-will-never-guess'  # Set securely 
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URI') or 'sqlite:///dyconcrete.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
