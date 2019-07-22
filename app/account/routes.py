import time
from datetime import datetime

import pytz
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, fresh_login_required, login_required

from app import db, limiter
from app.account import bp
from app.account.forms import AccountForm, PasswordForm
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
    return redirect(url_for('index'))
