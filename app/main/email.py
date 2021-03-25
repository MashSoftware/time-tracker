import requests
from flask import current_app, render_template
from requests.exceptions import RequestException
from werkzeug.exceptions import InternalServerError


def send_activation_email(user):
    token = user.generate_token(expires_in=3600)
    try:
        requests.post(
            "{0}/messages".format(current_app.config["MAILGUN_API_URL"]),
            auth=("api", current_app.config["MAILGUN_API_KEY"]),
            data={
                "from": "The Button <thebutton@mashsoftware.com>",
                "to": user.email_address,
                "subject": "Activate your account",
                "text": render_template("email/activation.txt", token=token),
                "html": render_template("email/activation.html", token=token),
            },
        )
        current_app.logger.info("Sent user {} activation email".format(user.id))
    except RequestException:
        current_app.logger.error("Error sending user {} activation email".format(user.id))
        raise InternalServerError


def send_confirmation_email(user):
    token = user.generate_token(expires_in=3600)
    try:
        requests.post(
            "{0}/messages".format(current_app.config["MAILGUN_API_URL"]),
            auth=("api", current_app.config["MAILGUN_API_KEY"]),
            data={
                "from": "The Button <thebutton@mashsoftware.com>",
                "to": user.email_address,
                "subject": "Confirm your email address",
                "text": render_template("email/confirmation.txt", token=token),
                "html": render_template("email/confirmation.html", token=token),
            },
        )
        current_app.logger.info("Sent user {} confirmation email".format(user.id))
    except RequestException:
        current_app.logger.error("Error sending user {} confirmation email".format(user.id))
        raise InternalServerError


def send_reset_password_email(user):
    token = user.generate_token()
    try:
        requests.post(
            "{0}/messages".format(current_app.config["MAILGUN_API_URL"]),
            auth=("api", current_app.config["MAILGUN_API_KEY"]),
            data={
                "from": "The Button <thebutton@mashsoftware.com>",
                "to": user.email_address,
                "subject": "Reset your password",
                "text": render_template("email/reset_password.txt", token=token),
                "html": render_template("email/reset_password.html", token=token),
            },
        )
        current_app.logger.info("Sent user {} reset password email".format(user.id))
    except RequestException:
        current_app.logger.error("Error sending user {} reset password email".format(user.id))
        raise InternalServerError
