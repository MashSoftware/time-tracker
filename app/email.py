import requests
from flask import render_template

from app import app


def send_reset_password_email(user):
    token = user.get_reset_password_token()
    return requests.post(
        '{0}/messages'.format(app.config['MAILGUN_API_URL']),
        auth=("api", app.config['MAILGUN_API_KEY']),
        data={
            "from": "The Button <mailgun@sandboxa445b3262e834e028a1c45d00bc714b1.mailgun.org>",
            "to": user.email_address,
            "subject": "Reset your password",
            "text": render_template('email/reset_password.txt', token=token),
            "html": render_template('email/reset_password.html', token=token)}
    )
