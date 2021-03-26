import unittest

import jwt
from app import create_app
from app.models import User
from flask import current_app


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(
            email_address="mash@example.com",
            password="8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f",
            timezone="Europe/London",
        )
        self.assertFalse(user.check_password("Haxx0rz"))
        self.assertTrue(user.check_password("8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f"))

    def test_token_generation(self):
        user = User(
            email_address="mash@example.com",
            password="8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f",
            timezone="Europe/London",
        )
        token = user.generate_token()
        self.assertTrue(jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"]))

    def test_change_password(self):
        user = User(
            email_address="mash@example.com",
            password="8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f",
            timezone="Europe/London",
        )
        user.set_password("yxxItMC*217XjWbz*a4&W@vK8h^qy!eZ")
        self.assertFalse(user.check_password("8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f"))
        self.assertTrue(user.check_password("yxxItMC*217XjWbz*a4&W@vK8h^qy!eZ"))

    def test_schedule(self):
        user = User(
            email_address="mash@example.com",
            password="8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f",
            timezone="Europe/London",
        )
        user.monday = 1
        user.tuesday = 2
        user.wednesday = 3
        user.thursday = 4
        user.friday = 5
        user.saturday = 6
        user.sunday = 7
        self.assertEqual(user.schedule(), 28)

    def test_schedule_string(self):
        user = User(
            email_address="mash@example.com",
            password="8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f",
            timezone="Europe/London",
        )
        user.monday = 1
        user.tuesday = 2
        user.wednesday = 3
        user.thursday = 4
        user.friday = 5
        user.saturday = 6
        user.sunday = 7
        self.assertEqual(user.schedule_string(), "28s")

    def test_schedule_decimal(self):
        user = User(
            email_address="mash@example.com",
            password="8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f",
            timezone="Europe/London",
        )
        user.monday = 1
        user.tuesday = 2
        user.wednesday = 3
        user.thursday = 4
        user.friday = 5
        user.saturday = 6
        user.sunday = 7
        self.assertEqual(user.schedule_decimal(), 0.0)
