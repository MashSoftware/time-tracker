import os


class Config(object):
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STORAGE_URI = os.environ.get("REDIS_URL")
    REMEMBER_COOKIE_DURATION = 2592000
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": 20}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VERSION_NUMBER = os.environ.get("VERSION_NUMBER")


class TestConfig(Config):
    TESTING = True
