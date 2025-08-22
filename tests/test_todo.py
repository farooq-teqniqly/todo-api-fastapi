def _create_user(client, fake):
    response = client.post("/users/", json={"email": fake.email()})
    data = response.json()
    user_id = data["id"]
    return user_id

def test_create_todo_when_user_not_found_return_404(client, fake):
    response = client.post("/todos/", json={"title": fake.sentence(2), "user_id": fake.random_int()})
    assert response.status_code == 404

def test_create_todo(client, fake):
    want_title = fake.sentence(2)
    user_id = _create_user(client, fake)

    response = client.post("/todos/", json={"title": want_title, "user_id": user_id})
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == want_title
    assert data["completed"] is False

    todo_id = data["id"]
    assert todo_id > 0
    want_location = f"http://testserver/todos/{todo_id}"
    assert response.headers["Location"] == want_location


def test_get_todos(client, fake):
    want_title = fake.sentence(2)
    user_id = _create_user(client, fake)

    client.post("/todos/", json={"title": want_title, "user_id": user_id})
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == want_title
    assert data[0]["completed"] is False
    assert data[0]["user_id"] == 1

def test_get_todo(client, fake):
    want_title = fake.sentence(2)
    user_id = _create_user(client, fake)
    response = client.post("/todos/", json={"title": want_title, "user_id": user_id})
    data = response.json()
    todo_id = data["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == want_title
    assert data["completed"] is False
    assert data["user_id"] == user_id

def test_update_todo_title(client, fake):
    original_title = fake.sentence(2)
    user_id = _create_user(client, fake)
    client.post("/todos/", json={"title": original_title, "user_id": user_id})
    todo_id = 1
    new_title = fake.sentence(2)
    response = client.put(f"/todos/{todo_id}", json={"title": new_title})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == new_title
    assert data["completed"] is False

def test_set_todo_completed(client, fake):
    want_title = fake.sentence(2)
    user_id = _create_user(client, fake)
    response = client.post("/todos/", json={"title": want_title, "user_id": user_id})
    data = response.json()
    todo_id = data["id"]
    response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == want_title
    assert data["completed"] is True