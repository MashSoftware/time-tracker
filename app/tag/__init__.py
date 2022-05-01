from flask import Blueprint

bp = Blueprint("tag", __name__, template_folder="../templates/tag")

from app.tag import routes  # noqa: E402,F401
