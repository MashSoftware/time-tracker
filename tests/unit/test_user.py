import jwt


def test_new_user(new_user):
    assert new_user.email_address == "mash@example.com"
    assert new_user.timezone == "Europe/London"


def test_password_hashing(new_user):
    assert new_user.check_password("Haxx0rz") is False
    assert new_user.check_password("8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f") is True


def test_token_generation(new_user):
    token = new_user.generate_token()
    assert jwt.decode(token, "!DAyH2qdEqmGzriZMvxU!wzTWql6UJ4P", algorithms=["HS256"]) is True


def test_change_password(new_user):
    new_user.set_password("yxxItMC*217XjWbz*a4&W@vK8h^qy!eZ")
    assert new_user.check_password("8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f") is False
    assert new_user.check_password("yxxItMC*217XjWbz*a4&W@vK8h^qy!eZ") is True


def test_schedule(new_user):
    new_user.monday = 1
    new_user.tuesday = 2
    new_user.wednesday = 3
    new_user.thursday = 4
    new_user.friday = 5
    new_user.saturday = 6
    new_user.sunday = 7
    assert new_user.schedule() == 28


def test_schedule_string(new_user):
    new_user.monday = 1
    new_user.tuesday = 2
    new_user.wednesday = 3
    new_user.thursday = 4
    new_user.friday = 5
    new_user.saturday = 6
    new_user.sunday = 7
    assert new_user.schedule_string() == "28s"


def test_schedule_decimal(new_user):
    new_user.monday = 1
    new_user.tuesday = 2
    new_user.wednesday = 3
    new_user.thursday = 4
    new_user.friday = 5
    new_user.saturday = 6
    new_user.sunday = 7
    assert new_user.schedule_decimal() == 0.0
