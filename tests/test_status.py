from .conftest import TestClient
from uuid import UUID

def test_create_status(client: TestClient):
    response = client.post(
        "/status/", json={"status": "Good"}
    )
    data = response.json()
    assert response.status_code == 201
    assert data["status"] == "Good"

def test_get_status(client: TestClient):
    response = client.post(
        "/status/", json={"status": "Good"}
    )
    assert response.status_code == 201

    response = client.get("/status/?offset=0&limit=100")
    data = response.json()
    assert response.status_code == 200
    assert data[0].get("status") == "Good" # tra ve 1 list dict status

def test_delete_status(client: TestClient):
    response = client.post(
        "/status/", json={"status": "Good"}
    )
    assert response.status_code == 201
    status_id = response.json()["id"]

    response = client.delete(f"/status/{status_id}")
    assert response.status_code == 204

def test_update_status(client: TestClient):
    response = client.post(
        "/status/", json={"status": "Good"}
    )
    assert response.status_code == 201
    status_id = response.json()["id"]

    updated_data = {
        "status": "Bad"
    }
    response = client.patch(f"/status/{status_id}", json=updated_data)
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "Bad"
