import os


class Config:
    """Base Flask configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'