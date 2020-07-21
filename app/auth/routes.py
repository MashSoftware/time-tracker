import time
from datetime import datetime

import pytz
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.forms import LoginForm, ResetPasswordForm, SignupForm, TokenRequestForm
from app.main.email import send_activation_email, send_confirmation_email, send_reset_password_email
from app.models import User


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("entry.entries"))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email_address=form.email_address.data, password=form.password.data, timezone=form.timezone.data,)
        db.session.add(user)
        db.session.commit()
        send_activation_email(user)
        flash(
            "Thanks for signing up! We've sent an email to {0} with instructions to activate your account.".format(
                user.email_address
            ),
            "success",
        )
        return redirect(url_for("main.index"))
    return render_template("auth/sign_up_form.html", title="Sign up", form=form)


@bp.route("/activate", methods=["GET", "POST"])
def activate_request():
    if current_user.is_authenticated:
        return redirect(url_for("entry.entries"))
    form = TokenRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user.activated_at is None:
            send_activation_email(user)
        else:
            send_confirmation_email(user)
        flash(
            "We've sent an email to {0} with instructions to activate your account.".format(form.email_address.data),
            "success",
        )
        return redirect(url_for("main.index"))
    return render_template("auth/activate_request_form.html", title="Activate account", form=form)


@bp.route("/activate/<token>")
def activate(token):
    if current_user.is_authenticated:
        return redirect(url_for("entry.entries"))
    user = User.verify_token(token)
    if not user:
        flash("The activation token is invalid, please request another.", "danger")
        return redirect(url_for("main.index"))
    user.activated_at = pytz.utc.localize(datetime.utcnow())
    db.session.commit()
    flash("Your account has been activated. Please log in to continue.", "success")
    return redirect(url_for("auth.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None or not user.check_password(form.password.data) or user.activated_at is None:
            time.sleep(1)
            flash("Invalid email address or password.", "danger")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        user.login_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("entry.entries")
        flash("You have logged in.", "success")
        return redirect(next_page)
    elif request.method == "GET" and current_user.is_authenticated:
        form.email_address.data = current_user.email_address
    return render_template("auth/log_in_form.html", title="Log in", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("You have logged out.", "success")
    return redirect(url_for("main.index"))


@bp.route("/reset-password", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("entry.entries"))
    form = TokenRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user:
            send_reset_password_email(user)
        flash(
            "We've sent an email to {0} with instructions to reset your password.".format(form.email_address.data),
            "success",
        )
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_request_form.html", title="Reset password", form=form)


@bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("entry.entries"))
    user = User.verify_token(token)
    if not user:
        flash("The password reset token is invalid, please request another.", "danger")
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        user.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.commit()
        flash("Your password has been reset, you may now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password_form.html", title="Reset password", form=form)
