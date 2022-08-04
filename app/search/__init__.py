from flask import Blueprint

bp = Blueprint("search", __name__, template_folder="../templates/search")

from app.search import routes  # noqa: E402,F401
