import os

from app.main import bp
from flask import current_app, redirect, render_template, send_from_directory, url_for
from flask_login import current_user
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
    return render_template("error.html", title="Oops!", error=error), error.code
