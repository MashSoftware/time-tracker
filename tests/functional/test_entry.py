def test_get_unauthenticated_entries_page(client):
    response = client.get("/entries", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
