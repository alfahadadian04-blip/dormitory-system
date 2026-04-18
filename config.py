import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///dormitory.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'adian'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'adian123'
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
