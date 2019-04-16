import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!DAyH2qdEqmGzriZMvxU!wzTWql6UJ4P'
