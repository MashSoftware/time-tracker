import requests

from app import app

# def send_reset_password_email(user):
#     token = user.get_reset_password_token()
#     send_email(
#         'The Button - Reset your password',
#         sender='the-button@mashsoftware.com',
#         recipients=[user.email_address],
#         text_body=render_template('email/reset_password.txt', user=user, token=token),
#         html_body=render_template('email/reset_password.html', user=user, token=token)
#     )


def send_simple_message():
    return requests.post(
        '{0}/messages'.format(app.config['MAILGUN_API_URL']),
        auth=("api", app.config['MAILGUN_API_KEY']),
        data={
            "from": "The Button <mailgun@sandboxa445b3262e834e028a1c45d00bc714b1.mailgun.org>",
            "to": "matt@mashsoftware.com",
            "subject": "Hello",
            "text": "Testing some Mailgun awesomness!"}
    )
