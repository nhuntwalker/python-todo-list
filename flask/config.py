"""."""
import os
basedir = os.path.dirname(__file__)


class Config(object):
    """."""

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'beautiful-sunshine')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'todo_flask')


class DevelopmentConfig(Config):
    """."""

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """."""

    TESTING = True


class ProductionConfig(Config):
    """."""

    DEBUG = False
