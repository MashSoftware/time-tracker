def test_index_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
