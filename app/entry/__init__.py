from flask import Blueprint

bp = Blueprint("entry", __name__, template_folder="../templates/entry")

from app.entry import routes  # noqa: E402,F401
