import os

from flask import (current_app, redirect, render_template, send_from_directory,
                   url_for)
from flask_login import current_user
from werkzeug.exceptions import HTTPException

from app.main import bp


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('entry.entries'))
    return render_template('index.html')


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@bp.route('/help')
def help():
    return render_template('help.html', title='Help')


@bp.app_errorhandler(HTTPException)
def forbidden(error):
    return render_template('error.html', title='Oops!', error=error), error.code
