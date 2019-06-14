import requests
from flask import render_template

from app import app


def send_activation_email(user):
    token = user.generate_token()
    return requests.post(
        '{0}/messages'.format(app.config['MAILGUN_API_URL']),
        auth=("api", app.config['MAILGUN_API_KEY']),
        data={
            "from": "The Button <thebutton@mashsoftware.com>",
            "to": user.email_address,
            "subject": "Activate your account",
            "text": render_template('email/activation.txt', token=token),
            "html": render_template('email/activation.html', token=token)}
    )


def send_reset_password_email(user):
    token = user.generate_token()
    return requests.post(
        '{0}/messages'.format(app.config['MAILGUN_API_URL']),
        auth=("api", app.config['MAILGUN_API_KEY']),
        data={
            "from": "The Button <thebutton@mashsoftware.com>",
            "to": user.email_address,
            "subject": "Reset your password",
            "text": render_template('email/reset_password.txt', token=token),
            "html": render_template('email/reset_password.html', token=token)}
    )
