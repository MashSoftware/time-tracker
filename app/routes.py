from flask import render_template

from app import app
from app.forms import LoginForm, SignupForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    form = SignupForm()
    return render_template('sign_up.html', title='Sign up', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('log_in.html', title='Log in', form=form)
