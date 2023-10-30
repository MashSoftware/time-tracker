def test_get_unauthenticated_account_page(client):
    response = client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
