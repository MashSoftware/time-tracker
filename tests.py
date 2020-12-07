import unittest

from app.models import User
from app.utils import seconds_to_decimal, seconds_to_string


class UtilsCase(unittest.TestCase):
    def test_seconds_to_string(self):
        seconds = 26640
        self.assertEqual(seconds_to_string(seconds), "7 h 24 min")

    def test_seconds_to_decimal(self):
        seconds = 26640
        self.assertEqual(seconds_to_decimal(seconds), 7.4)


class UserModelCase(unittest.TestCase):
    def test_password_hashing(self):
        user = User(
            email_address="mash@example.com", password="8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f", timezone="Europe/London"
        )
        self.assertFalse(user.check_password("Haxx0rz"))
        self.assertTrue(user.check_password("8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
