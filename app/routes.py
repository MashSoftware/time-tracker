from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, SignupForm
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email_address=form.email_address.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Thanks for signing up {}!'.format(user.first_name), 'success')
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Sign up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email address or password.', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Welcome back {}.'.format(current_user.first_name), 'success')
        return redirect(url_for('index'))
    return render_template('log_in.html', title='Log in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('index'))
