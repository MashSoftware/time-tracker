import unittest
from datetime import datetime

from app import create_app
from app.models import Event


class EventModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_duration(self):
        started_at = datetime(2020, 1, 1, 9, 0, 0)
        ended_at = datetime(2020, 1, 1, 9, 1, 0)
        event = Event("34032588-6d99-42ff-b8a6-613bba5c211c", started_at)

        self.assertEqual(event.duration(), 0)
        self.assertEqual(event.duration(end=ended_at), 60)
        event.ended_at = ended_at
        self.assertEqual(event.duration(), 60)

    def test_duration_string(self):
        started_at = datetime(2020, 1, 1, 9, 0, 0)
        ended_at = datetime(2020, 1, 1, 9, 1, 0)
        event = Event("34032588-6d99-42ff-b8a6-613bba5c211c", started_at)

        self.assertEqual(event.duration_string(), "0s")
        self.assertEqual(event.duration_string(end=ended_at), "1 min")
        event.ended_at = ended_at
        self.assertEqual(event.duration_string(), "1 min")

    def test_duration_decimal(self):
        started_at = datetime(2020, 1, 1, 9, 0, 0)
        ended_at = datetime(2020, 1, 1, 9, 1, 0)
        event = Event("34032588-6d99-42ff-b8a6-613bba5c211c", started_at)

        self.assertEqual(event.duration_decimal(), 0.0)
        self.assertEqual(event.duration_decimal(end=ended_at), 0.01)
        event.ended_at = ended_at
        self.assertEqual(event.duration_decimal(), 0.01)
