import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    load_dotenv(os.path.join(basedir, ".flaskenv"))
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    MAILGUN_API_URL = os.environ.get("MAILGUN_API_URL")
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL") or "memory://"
    REMEMBER_COOKIE_DURATION = 2592000
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
        if os.environ.get("DATABASE_URL")
        else "postgresql://mash:mash@localhost:5432/button"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": 20}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VERSION_NUMBER = os.environ.get("VERSION_NUMBER")


class TestConfig(Config):
    TESTING = True
