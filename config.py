import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!DAyH2qdEqmGzriZMvxU!wzTWql6UJ4P'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://clickuser:clickpassword@localhost:5432/click'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'memory://'
    RATELIMIT_HEADERS_ENABLED = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
