import requests
from flask import current_app, render_template
from requests.exceptions import RequestException
from werkzeug.exceptions import InternalServerError


def send_activation_email(user):
    token = user.generate_token(expires_in=3600)
    try:
        requests.post(
            f"{current_app.config['MAILGUN_API_URL']}/messages",
            auth=("api", current_app.config["MAILGUN_API_KEY"]),
            data={
                "from": "Mash Time Tracker <timetracker@mashsoftware.com>",
                "to": user.email_address,
                "subject": "Activate your account",
                "text": render_template("email/activation.txt", token=token),
                "html": render_template("email/activation.html", token=token),
            },
            timeout=10,
        )
        current_app.logger.info(f"Sent user {user.id} activation email")
    except RequestException:
        current_app.logger.error(f"Error sending user {user.id} activation email")
        raise InternalServerError


def send_confirmation_email(user):
    token = user.generate_token(expires_in=3600)
    try:
        requests.post(
            f"{current_app.config['MAILGUN_API_URL']}/messages",
            auth=("api", current_app.config["MAILGUN_API_KEY"]),
            data={
                "from": "Mash Time Tracker <timetracker@mashsoftware.com>",
                "to": user.email_address,
                "subject": "Confirm your email address",
                "text": render_template("email/confirmation.txt", token=token),
                "html": render_template("email/confirmation.html", token=token),
            },
            timeout=10,
        )
        current_app.logger.info(f"Sent user {user.id} confirmation email")
    except RequestException:
        current_app.logger.error(f"Error sending user {user.id} confirmation email")
        raise InternalServerError


def send_reset_password_email(user):
    token = user.generate_token()
    try:
        requests.post(
            f"{current_app.config['MAILGUN_API_URL']}/messages",
            auth=("api", current_app.config["MAILGUN_API_KEY"]),
            data={
                "from": "Mash Time Tracker <timetracker@mashsoftware.com>",
                "to": user.email_address,
                "subject": "Reset your password",
                "text": render_template("email/reset_password.txt", token=token),
                "html": render_template("email/reset_password.html", token=token),
            },
            timeout=10,
        )
        current_app.logger.info(f"Sent user {user.id} reset password email")
    except RequestException:
        current_app.logger.error(f"Error sending user {user.id} reset password email")
        raise InternalServerError
