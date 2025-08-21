def test_create_todo(client, fake):
    want_title = fake.sentence(2)
    response = client.post("/todos/", json={"title": want_title})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == want_title
    assert data["completed"] is False

    todo_id = data["id"]
    assert todo_id != 0
    want_location = f"http://testserver/todos/{todo_id}"
    assert response.headers["Location"] == want_location


def test_get_todos(client, fake):
    want_title = fake.sentence(2)
    client.post("/todos/", json={"title": want_title})
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == want_title
    assert data[0]["completed"] is False

def test_get_todo(client, fake):
    want_title = fake.sentence(2)
    client.post("/todos/", json={"title": want_title})
    todo_id = 1
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == want_title
    assert data["completed"] is False

def test_update_todo_title(client, fake):
    original_title = fake.sentence(2)
    client.post("/todos/", json={"title": original_title})
    todo_id = 1
    new_title = fake.sentence(2)
    response = client.put(f"/todos/{todo_id}", json={"title": new_title})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == new_title
    assert data["completed"] is False

def test_set_todo_completed(client, fake):
    want_title = fake.sentence(2)
    client.post("/todos/", json={"title": want_title})
    todo_id = 1
    response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == want_title
    assert data["completed"] is True