import app
from starlette.testclient import TestClient

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/login", json={
        "username": "doctor1",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post("/auth/login", json={
        "username": "invalid",
        "password": "wrong"
    })
    assert response.status_code == 401
