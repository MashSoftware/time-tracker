def test_get_unauthenticated_locations_page(client):
    response = client.get("/locations")
    assert response.status_code == 308
