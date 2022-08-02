from app.models import Tag


def test_new_tag(new_user):
    new_tag = Tag(user_id=new_user.id, name="New Tag")
    assert new_tag.user_id == new_user.id
    assert new_tag.name == "New Tag"
