def test_create_user(client, fake):
    want_email = fake.email()
    response = client.post("/users/", json={"email": want_email})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == want_email

    user_id = data["id"]
    assert user_id != 0
    want_location = f"http://testserver/users/{user_id}"
    assert response.headers["Location"] == want_location

def test_get_user(client, fake):
    want_email = fake.email()
    response = client.post("/users/", json={"email": want_email})
    data = response.json()
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == want_email

def test_when_email_already_exists_return_400(client, fake):
    email = fake.email()
    client.post("/users/", json={"email": email})
    response = client.post("/users/", json={"email": email})
    assert response.status_code == 400

def test_when_email_not_valid_return_400(client, fake):
    email = fake.word()
    client.post("/users/", json={"email": email})
    response = client.post("/users/", json={"email": email})
    assert response.status_code == 422