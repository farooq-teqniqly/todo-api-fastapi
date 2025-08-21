def test_create_todo(client):
    response = client.post("/todos/", json={"title": "Test from container"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test from container"
    assert data["completed"] is False