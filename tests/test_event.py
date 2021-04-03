import unittest
from datetime import datetime

from app.models import Event


class EventModelCase(unittest.TestCase):
    def test_duration(self):
        started_at = datetime(2020, 1, 1, 9, 0, 0)
        ended_at = datetime(2020, 1, 1, 9, 1, 0)
        event = Event("34032588-6d99-42ff-b8a6-613bba5c211c", started_at)

        assert event.duration() == 0
        assert event.duration(end=ended_at) == 60
        event.ended_at = ended_at
        assert event.duration() == 60

    def test_duration_string(self):
        started_at = datetime(2020, 1, 1, 9, 0, 0)
        ended_at = datetime(2020, 1, 1, 9, 1, 0)
        event = Event("34032588-6d99-42ff-b8a6-613bba5c211c", started_at)

        assert event.duration_string() == "0s"
        assert event.duration_string(end=ended_at) == "1 min"
        event.ended_at = ended_at
        assert event.duration_string() == "1 min"

    def test_duration_decimal(self):
        started_at = datetime(2020, 1, 1, 9, 0, 0)
        ended_at = datetime(2020, 1, 1, 9, 1, 0)
        event = Event("34032588-6d99-42ff-b8a6-613bba5c211c", started_at)

        assert event.duration_decimal() == 0.0
        assert event.duration_decimal(end=ended_at) == 0.01
        event.ended_at = ended_at
        assert event.duration_decimal() == 0.01
