def test_get_unauthenticated_search_page(client):
    response = client.get("/search", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
