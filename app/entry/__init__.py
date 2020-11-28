from flask import Blueprint

bp = Blueprint("entry", __name__)

from app.entry import routes
