import pytest
from app import db, create_app
from config import TestConfig

url = "http://localhost:25565"

@pytest.fixture(scope='function', autouse=True)
def setup_function():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
    app.testing = True
    global client
    client = app.test_client()

    yield

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_register():
    test_data1 = {"username": "User1", "password": "password"}
    response1 = client.post("/register", json=test_data1)

    test_data2 = {"username": "User2", "password": "password"}
    response2 = client.post("/register", json=test_data2)

    assert response1.get_json()["message"] == "Registered successfully"
    assert response2.get_json()["message"] == "Registered successfully"

def test_login():
    test_data = {"username": "User1", "password": "password"}
    client.post("/register", json=test_data)

    response = client.post("/login", json=test_data)
    assert response.get_json()["message"] == "Logged in successfully"

def test_invalid_login():
    test_data = {"username": "User1", "password": "password"}
    client.post("/register", json=test_data)

    test_data["password"] = "wrongpass"
    response = client.post("/login", json=test_data)
    assert response.get_json()["message"] == "Invalid credentials"

def test_logout():
    test_data = {"username": "User1", "password": "password"}
    client.post("/register", json=test_data)
    client.post("/login", json=test_data)

    response = client.get("/logout")
    assert response.get_json()["message"] == "Logged out successfully"

def test_send_message():
    test_data1 = {"username": "User1", "password": "password"}
    client.post("/register", json=test_data1)
    test_data2 = {"username": "User2", "password": "password"}
    client.post("/register", json=test_data2)

    client.post("login", json=test_data1)

    message_data = {"recipient": "User2", "message": "Hello, User2!"}
    response = client.post("/send_message", json=message_data)
    assert response.get_json()["message"] == "Message sent"

def test_send_message_to_nonexistent_user():
    test_data = {"username": "User1", "password": "password"}
    client.post("/register", json=test_data)
    client.post("/login", json=test_data)

    message_data = {"recipient": "NonexistentUser", "message": "Hello!"}
    response = client.post("/send_message", json=message_data)
    assert response.get_json()["message"] == "Recipient not found"

def test_get_messages():
    test_data1 = {"username": "User1", "password": "password"}
    client.post("/register", json=test_data1)
    test_data2 = {"username": "User2", "password": "password"}
    client.post("/register", json=test_data2)

    client.post("/login", json=test_data1)
    message_data = {"recipient": "User2", "message": "Hello, User2!"}
    client.post("/send_message", json=message_data)

    get_messages_data = {"recipient": "User2"}
    response = client.post("/get_messages", json=get_messages_data)
    messages = response.get_json()["messages"]

    assert any(msg['sender'] == 'User1' and msg['recipient'] == 'User2' and msg['body'] == 'Hello, User2!' for msg in messages)