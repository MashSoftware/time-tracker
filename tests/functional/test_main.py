def test_get_index_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_get_help_page(client):
    response = client.get("/help")
    assert response.status_code == 200

def test_get_cookies_page(client):
    response = client.get("/cookies")
    assert response.status_code == 200