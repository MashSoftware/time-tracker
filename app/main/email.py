import requests
from flask import current_app, render_template


def send_activation_email(user):
    token = user.generate_token(expires_in=3600)
    return requests.post(
        '{0}/messages'.format(current_app.config['MAILGUN_API_URL']),
        auth=("api", current_app.config['MAILGUN_API_KEY']),
        data={
            "from": "The Button <thebutton@mashsoftware.com>",
            "to": user.email_address,
            "subject": "Activate your account",
            "text": render_template('email/activation.txt', token=token),
            "html": render_template('email/activation.html', token=token)}
    )


def send_confirmation_email(user):
    token = user.generate_token(expires_in=3600)
    return requests.post(
        '{0}/messages'.format(current_app.config['MAILGUN_API_URL']),
        auth=("api", current_app.config['MAILGUN_API_KEY']),
        data={
            "from": "The Button <thebutton@mashsoftware.com>",
            "to": user.email_address,
            "subject": "Confirm your email address",
            "text": render_template('email/confirmation.txt', token=token),
            "html": render_template('email/confirmation.html', token=token)}
    )


def send_reset_password_email(user):
    token = user.generate_token()
    return requests.post(
        '{0}/messages'.format(current_app.config['MAILGUN_API_URL']),
        auth=("api", current_app.config['MAILGUN_API_KEY']),
        data={
            "from": "The Button <thebutton@mashsoftware.com>",
            "to": user.email_address,
            "subject": "Reset your password",
            "text": render_template('email/reset_password.txt', token=token),
            "html": render_template('email/reset_password.html', token=token)}
    )
