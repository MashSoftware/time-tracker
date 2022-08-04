from flask import Blueprint

bp = Blueprint("main", __name__, template_folder="../templates/main")

from app.main import email, routes  # noqa: E402,F401
