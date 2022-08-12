from datetime import datetime

from app.models import Location


def test_new_location(client, new_user):
    new_location = Location(user_id=new_user.id, name="New Location")
    assert new_location.user_id == new_user.id
    assert new_location.name == "New Location"
    assert type(new_location.created_at) == datetime
    assert new_location.updated_at is None
