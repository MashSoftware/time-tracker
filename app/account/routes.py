from datetime import date, datetime, timedelta

import pytz
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, fresh_login_required, login_required

from app import csrf, db, limiter
from app.account import bp
from app.account.forms import AccountForm, PasswordForm, ScheduleForm
from app.main.email import send_confirmation_email
from app.utils import seconds_to_time


@bp.route("/")
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def account():
    user = current_user
    user.created_at = user.created_at.astimezone(pytz.timezone(user.timezone))
    user.login_at = user.login_at.astimezone(pytz.timezone(user.timezone))
    user.updated_at = user.updated_at.astimezone(pytz.timezone(user.timezone)) if user.updated_at else None
    history_date = datetime.utcnow().astimezone(pytz.timezone(user.timezone)) - timedelta(weeks=user.entry_history)
    return render_template("account.html", title="My Account", user=user, history_date=history_date)


@bp.route("/change-password", methods=["GET", "POST"])
@fresh_login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            current_user.updated_at = pytz.utc.localize(datetime.utcnow())
            db.session.add(current_user)
            db.session.commit()
            flash("Your password has been changed.", "success")
            current_app.logger.info("User {} changed password".format(current_user.id))
        else:
            flash("Invalid password.", "danger")
            current_app.logger.warning("User {} change password failed".format(current_user.id))
            return redirect(url_for("account.change_password"))
        return redirect(url_for("account.account"))

    return render_template("change_password_form.html", title="Change password", form=form)


@bp.route("/update", methods=["GET", "POST"])
@fresh_login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def update():
    form = AccountForm()
    if form.validate_on_submit():
        if form.email_address.data != current_user.email_address:
            current_user.email_address = form.email_address.data
            current_user.activated_at = None
            send_confirmation_email(current_user)
            flash(
                "We've sent an email to {0} with instructions to confirm your email address.".format(
                    current_user.email_address
                ),
                "success",
            )
        current_user.timezone = form.timezone.data
        current_user.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(current_user)
        db.session.commit()
        flash("Account changes have been saved.", "success")
        current_app.logger.info("User {} updated account".format(current_user.id))
        return redirect(url_for("account.account"))
    elif request.method == "GET":
        form.email_address.data = current_user.email_address
        form.timezone.data = current_user.timezone
    return render_template("account_form.html", title="Edit account", form=form)


@bp.route("/delete", methods=["GET", "POST"])
@csrf.exempt
@fresh_login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def delete():
    if request.method == "GET":
        return render_template("delete_account.html", title="Delete account")
    elif request.method == "POST":
        current_app.logger.info("User {} deleted account".format(current_user.id))
        db.session.delete(current_user)
        db.session.commit()
        flash(
            "Your account and all personal information has been permanently deleted.",
            "success",
        )
        return redirect(url_for("main.index"))


@bp.route("/schedule", methods=["GET", "POST"])
@fresh_login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
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
        current_user.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(current_user)
        db.session.commit()
        current_app.logger.info("User {} updated schedule".format(current_user.id))
        flash("Schedule changes have been saved", "success")
        return redirect(url_for("account.account"))
    elif request.method == "GET":
        form.monday.data = seconds_to_time(current_user.monday)
        form.tuesday.data = seconds_to_time(current_user.tuesday)
        form.wednesday.data = seconds_to_time(current_user.wednesday)
        form.thursday.data = seconds_to_time(current_user.thursday)
        form.friday.data = seconds_to_time(current_user.friday)
        form.saturday.data = seconds_to_time(current_user.saturday)
        form.sunday.data = seconds_to_time(current_user.sunday)
    return render_template("schedule_form.html", title="Edit schedule", form=form)
