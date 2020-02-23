from flask import redirect, render_template, url_for
from flask_login import current_user
from werkzeug.exceptions import HTTPException

from app.main import bp


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('entry.entries'))
    return render_template('index.html')


@bp.route('/help')
def help():
    return render_template('help.html', title='Help')


@bp.app_errorhandler(HTTPException)
def http_error(error):
    return render_template('error.html', title='Oops!', error=error), error.code
