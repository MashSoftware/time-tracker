def test_get_signup_page(client):
    response = client.get("/signup")
    assert response.status_code == 200

def test_get_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_get_reset_password_page(client):
    response = client.get("/reset-password")
    assert response.status_code == 200