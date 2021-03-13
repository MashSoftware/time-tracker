import os

from app.main import bp
from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("entry.weekly"))
    return render_template("index.html")


@bp.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, "static"),
        "favicon.ico",
        mimetype="image/x-icon",
    )


@bp.route("/apple-touch-icon.png")
def apple_touch_icon():
    return send_from_directory(
        os.path.join(current_app.root_path, "static"),
        "apple-touch-icon.png",
        mimetype="image/png",
    )


@bp.route("/help")
def help():
    return render_template("help.html", title="Help")


@bp.app_errorhandler(HTTPException)
def http_error(error):
    current_app.logger.error("{}: {} - {}".format(error.code, error.name, request.url))
    return render_template("error.html", title=error.name, error=error), error.code


@bp.app_errorhandler(CSRFError)
def handle_csrf_error(error):
    current_app.logger.error("{}: {} - {}".format(error.code, error.description, request.url))
    flash("The form you were submitting has expired. Please try again.", "info")
    return redirect(request.full_path)
