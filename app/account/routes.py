import time
from datetime import date, datetime, time

import pytz
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, fresh_login_required, login_required

from app import db, limiter
from app.account import bp
from app.account.forms import AccountForm, PasswordForm, ScheduleForm
from app.main.email import send_confirmation_email


@bp.route('/')
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def account():
    user = current_user
    user.created_at = user.created_at.astimezone(pytz.timezone(user.timezone))
    user.login_at = user.login_at.astimezone(pytz.timezone(user.timezone))
    user.updated_at = user.updated_at.astimezone(pytz.timezone(user.timezone)) if user.updated_at else None
    return render_template('account/account.html', title='My Account', user=user)


@bp.route('/change-password', methods=['GET', 'POST'])
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
            time.sleep(1)
            flash('Invalid password.', 'danger')
            return redirect(url_for('account.change_password'))
        return redirect(url_for('account.account'))

    return render_template('account/change_password_form.html', title='Change password', form=form)


@bp.route('/update', methods=['GET', 'POST'])
@fresh_login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def update():
    form = AccountForm()
    if form.validate_on_submit():
        if form.email_address.data != current_user.email_address:
            current_user.email_address = form.email_address.data
            current_user.activated_at = None
            send_confirmation_email(current_user)
            flash("We've sent an email to {0} with instructions to confirm your email address."
                  .format(current_user.email_address), 'success')
        current_user.timezone = form.timezone.data
        current_user.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(current_user)
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account.account'))
    elif request.method == 'GET':
        form.email_address.data = current_user.email_address
        form.timezone.data = current_user.timezone
    return render_template('account/account_form.html', title='Update account', form=form)


@bp.route('/delete')
@fresh_login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def delete():
    db.session.delete(current_user)
    db.session.commit()
    flash('Your account and all personal information has been permanently deleted.', 'success')
    return redirect(url_for('main.index'))


@bp.route('/schedule', methods=['GET', 'POST'])
@fresh_login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        current_user.monday = (datetime.combine(date.min, form.monday.data) - datetime.min).total_seconds()
        current_user.tuesday = (datetime.combine(date.min, form.tuesday.data) - datetime.min).total_seconds()
        current_user.wednesday = (datetime.combine(date.min, form.wednesday.data) - datetime.min).total_seconds()
        current_user.thursday = (datetime.combine(date.min, form.thursday.data) - datetime.min).total_seconds()
        current_user.friday = (datetime.combine(date.min, form.friday.data) - datetime.min).total_seconds()
        current_user.saturday = (datetime.combine(date.min, form.saturday.data) - datetime.min).total_seconds()
        current_user.sunday = (datetime.combine(date.min, form.sunday.data) - datetime.min).total_seconds()
        db.session.add(current_user)
        db.session.commit()
        flash('Your schedule has been updated', 'success')
        return redirect(url_for('account.account'))
    elif request.method == 'GET':
        mon_hours, mon_remainder = divmod(current_user.monday, 3600)
        mon_minutes, mon_seconds = divmod(mon_remainder, 60)
        form.monday.data = time(hour=mon_hours, minute=mon_minutes, second=mon_seconds)

        tue_hours, tue_remainder = divmod(current_user.tuesday, 3600)
        tue_minutes, tue_seconds = divmod(tue_remainder, 60)
        form.tuesday.data = time(hour=tue_hours, minute=tue_minutes, second=tue_seconds)

        wed_hours, wed_remainder = divmod(current_user.wednesday, 3600)
        wed_minutes, wed_seconds = divmod(wed_remainder, 60)
        form.wednesday.data = time(hour=wed_hours, minute=wed_minutes, second=wed_seconds)

        thu_hours, thu_remainder = divmod(current_user.thursday, 3600)
        thu_minutes, thu_seconds = divmod(thu_remainder, 60)
        form.thursday.data = time(hour=thu_hours, minute=thu_minutes, second=thu_seconds)

        fri_hours, fri_remainder = divmod(current_user.friday, 3600)
        fri_minutes, fri_seconds = divmod(fri_remainder, 60)
        form.friday.data = time(hour=fri_hours, minute=fri_minutes, second=fri_seconds)

        sat_hours, sat_remainder = divmod(current_user.saturday, 3600)
        sat_minutes, sat_seconds = divmod(sat_remainder, 60)
        form.saturday.data = time(hour=sat_hours, minute=sat_minutes, second=sat_seconds)

        sun_hours, sun_remainder = divmod(current_user.sunday, 3600)
        sun_minutes, sun_seconds = divmod(sun_remainder, 60)
        form.sunday.data = time(hour=sun_hours, minute=sun_minutes, second=sun_seconds)
    return render_template('account/schedule_form.html', title='Update schedule', form=form)
