from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/help')
def help():
    return render_template('help.html', title='Help')
