import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!DAyH2qdEqmGzriZMvxU!wzTWql6UJ4P'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://clickuser:clickpassword@localhost:5432/click'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'memory://'
    RATELIMIT_HEADERS_ENABLED = True
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_API_URL = os.environ.get('MAILGUN_API_URL')
