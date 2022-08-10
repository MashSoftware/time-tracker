def test_get_unauthenticated_tags_page(client):
    response = client.get("/tags")
    assert response.status_code == 308
