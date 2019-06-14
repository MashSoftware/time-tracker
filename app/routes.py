import time
from datetime import datetime

import pytz
from flask import flash, redirect, render_template, request, url_for
from flask_login import (current_user, fresh_login_required, login_required,
                         login_user, logout_user)
from werkzeug.exceptions import Forbidden
from werkzeug.urls import url_parse

from app import app, db, limiter
from app.email import send_reset_password_email
from app.forms import (AccountForm, EventForm, LoginForm, PasswordForm,
                       ResetPasswordForm, ResetPasswordRequestForm, SignupForm)
from app.models import Event, User


@app.route('/')
def index():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        events = Event.query.filter_by(user_id=current_user.id).order_by(Event.started_at.desc()).paginate(page, 10, True)
        last_event = Event.query.filter_by(user_id=current_user.id).order_by(Event.started_at.desc()).first()
        if (last_event and last_event.ended_at) or last_event is None:
            start = True
        else:
            start = False
        for event in events.items:
            event.started_at = event.started_at.astimezone(pytz.timezone(current_user.timezone))
            if event.ended_at:
                event.ended_at = event.ended_at.astimezone(pytz.timezone(current_user.timezone))
        return render_template('index.html', events=events, start=start)
    else:
        return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            email_address=form.email_address.data,
            password=form.password.data,
            timezone=form.timezone.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for signing up! Please log in to continue.', 'success')
        return redirect(url_for('login'))
    return render_template('sign_up_form.html', title='Sign up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None or not user.check_password(form.password.data):
            time.sleep(1)
            flash('Invalid email address or password.', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        user.login_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('Welcome back.', 'success')
        return redirect(next_page)
    elif request.method == 'GET' and current_user.is_authenticated:
        form.email_address.data = current_user.email_address
    return render_template('log_in_form.html', title='Log in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user:
            send_reset_password_email(user)
        flash('Please check your email for instructions to reset your password.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password_request_form.html', title='Reset password', form=form)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token(token)
    if not user:
        flash('The password reset token is invalid, please request another.', 'danger')
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        user.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.commit()
        flash('Your password has been reset, you may now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password_form.html', title='Reset password', form=form)


@app.route('/account')
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def account():
    user = current_user
    user.created_at = user.created_at.astimezone(pytz.timezone(user.timezone))
    user.login_at = user.login_at.astimezone(pytz.timezone(user.timezone))
    user.updated_at = user.updated_at.astimezone(pytz.timezone(user.timezone)) if user.updated_at else None
    return render_template('account.html', title='My Account', user=user)


@app.route('/account/delete')
@fresh_login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    flash('Your account and all personal information has been permanently deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/account/change-password', methods=['GET', 'POST'])
@fresh_login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            current_user.updated_at = pytz.utc.localize(datetime.utcnow())
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been changed.', 'success')
        else:
            flash('Invalid password.', 'danger')
            return redirect(url_for('change_password'))
        return redirect(url_for('account'))

    return render_template('change_password_form.html', title='Change password', form=form)


@app.route('/account/update', methods=['GET', 'POST'])
@fresh_login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def update_account():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.email_address = form.email_address.data
        current_user.timezone = form.timezone.data
        current_user.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(current_user)
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email_address.data = current_user.email_address
        form.timezone.data = current_user.timezone
    return render_template('account_form.html', title='Update account', form=form)


@app.route('/entry')
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def create_event():
    event = Event.query.filter_by(user_id=current_user.id).order_by(Event.started_at.desc()).first()
    if event and event.ended_at is None:
        event.ended_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(event)
    else:
        new_event = Event(
            user_id=current_user.id,
            started_at=pytz.utc.localize(datetime.utcnow()))
        db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/entry/manual', methods=['GET', 'POST'])
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def manual_event():
    form = EventForm()
    if form.validate_on_submit():
        locale_started_at = pytz.timezone(current_user.timezone).localize(form.started_at.data)
        utc_started_at = locale_started_at.astimezone(pytz.utc)
        event = Event(user_id=current_user.id, started_at=utc_started_at)
        if form.ended_at.data:
            locale_ended_at = pytz.timezone(current_user.timezone).localize(form.ended_at.data)
            utc_ended_at = locale_ended_at.astimezone(pytz.utc)
            event.ended_at = utc_ended_at
        else:
            event.ended_at = None
        db.session.add(event)
        db.session.commit()
        flash('Time entry has been added.', 'success')
        return redirect(url_for('index'))
    return render_template('create_event_form.html', title='Create time entry', form=form)


@app.route('/entry/<uuid:id>/delete')
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def delete_event(id):
    event = Event.query.get_or_404(str(id))
    if event not in current_user.events:
        raise Forbidden()
    db.session.delete(event)
    db.session.commit()
    flash('Time entry has been deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/entry/<uuid:id>', methods=['GET', 'POST'])
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def update_event(id):
    event = Event.query.get_or_404(str(id))
    if event not in current_user.events:
        raise Forbidden()
    form = EventForm()
    if form.validate_on_submit():
        locale_started_at = pytz.timezone(current_user.timezone).localize(form.started_at.data)
        utc_started_at = locale_started_at.astimezone(pytz.utc)
        event.started_at = utc_started_at
        if form.ended_at.data:
            locale_ended_at = pytz.timezone(current_user.timezone).localize(form.ended_at.data)
            utc_ended_at = locale_ended_at.astimezone(pytz.utc)
            event.ended_at = utc_ended_at
        else:
            event.ended_at = None
        db.session.add(event)
        db.session.commit()
        flash('Time entry has been updated.', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        # Show timestamp in users localised timezone
        form.started_at.data = event.started_at.astimezone(pytz.timezone(current_user.timezone))
        if event.ended_at:
            form.ended_at.data = event.ended_at.astimezone(pytz.timezone(current_user.timezone))
    return render_template('update_event_form.html', title='Edit time entry', form=form, event=event)
