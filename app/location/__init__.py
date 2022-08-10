from flask import Blueprint

bp = Blueprint("location", __name__, template_folder="../templates/location")

from app.location import routes  # noqa: E402,F401
