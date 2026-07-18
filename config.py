import os
import warnings

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        warnings.warn(
            'SECRET_KEY environment variable is not set. '
            'Set SECRET_KEY in your .env file or environment variables. '
            'Using an insecure fallback for development only.',
            RuntimeWarning
        )
        SECRET_KEY = 'forecastiq-dev-key-do-not-use-in-production'

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'instance', 'forecastiq.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 86400
    SESSION_COOKIE_NAME = 'forecastiq_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    UPLOAD_FOLDER = os.path.join(basedir, 'data', 'uploads')
    EDA_REPORTS_FOLDER = os.path.join(basedir, 'reports', 'eda_reports')
    PROCESSED_FOLDER = os.path.join(basedir, 'data', 'processed')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
