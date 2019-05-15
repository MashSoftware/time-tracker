import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!DAyH2qdEqmGzriZMvxU!wzTWql6UJ4P'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://clickuser:clickpassword@localhost:5432/click'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL') or 'memory://'
