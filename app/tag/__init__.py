from flask import Blueprint

bp = Blueprint("tag", __name__)

from app.tag import routes
