def test_get_unauthenticated_locations_page(client):
    response = client.get("/locations", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
