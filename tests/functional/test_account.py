def test_get_unauthenticated_account_page(client):
    response = client.get("/account")
    assert response.status_code == 308