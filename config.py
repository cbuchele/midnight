import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../output/midnight.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False