from flask import render_template
from werkzeug.exceptions import HTTPException

from app import app


@app.errorhandler(HTTPException)
def forbidden(error):
    return render_template('error.html', title='Oops!', error=error), error.code
