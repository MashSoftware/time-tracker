def test_get_unauthenticated_search_page(client):
    response = client.get("/search")
    assert response.status_code == 308
