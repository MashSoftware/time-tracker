def test_get_unauthenticated_entries_page(client):
    response = client.get("/entries")
    assert response.status_code == 308