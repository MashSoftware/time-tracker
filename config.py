import os


class Config(object):
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    MAILGUN_API_URL = os.environ.get("MAILGUN_API_URL")
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get("REDIS_URL") or "memory://"
    RELEASE_DATE = os.environ.get("RELEASE_DATE")
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "!DAyH2qdEqmGzriZMvxU!wzTWql6UJ4P"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://mash:mash@localhost:5432/button"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": 20}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VERSION_NUMBER = os.environ.get("VERSION_NUMBER")
