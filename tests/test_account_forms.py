import unittest

from app import create_app
from app.account.forms import AccountForm, PasswordForm, ScheduleForm


class AccountFormsCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_account_form(self):
        with self.app.test_request_context('/'):
            form = AccountForm()
            form.email_address.data = "mash@example.com"
            form.timezone = "Europe/London"
            validated = form.validate()
            assert validated is True

    # def test_password_form(self):
    #     form = PasswordForm()

    # def test_schedule_form(self):
    #     form = ScheduleForm()
