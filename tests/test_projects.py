from .conftest import TestClient
from uuid import UUID

def test_create_project(client: TestClient):
    response = client.post(
        "/projects/", json={"name": "Project 1", "description": "Description 1"}
    )
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Project 1"
    assert data["description"] == "Description 1"

def test_get_projects(client: TestClient):
    response = client.post(
        "/projects/", json={"name": "Project 1", "description": "Description 1"}
    )
    assert response.status_code == 201

    response = client.get("/projects/?offset=0&limit=100")
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0

def test_delete_project(client: TestClient):
    response = client.post(
        "/projects/", json={"name": "Project 1", "description": "Description 1"}
    )
    assert response.status_code == 201
    project_id = response.json()["id"]

    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 204

def test_get_project_by_id(client: TestClient):
    response = client.post(
        "/projects/", json={"name": "Project 1", "description": "Description 1"}
    )
    assert response.status_code == 201
    project_id = response.json()["id"]

    response = client.get(f"/projects/{project_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Project 1"
    assert data["description"] == "Description 1"

def test_update_project(client: TestClient):
    response = client.post(
        "/projects/", json={"name": "Project 1", "description": "Description 1"}
    )
    assert response.status_code == 201
    project_id = response.json()["id"]

    updated_data = {
        "name": "Project 2",
        "description": "Description 2"
    }
    response = client.patch(f"/projects/{project_id}", json=updated_data)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Project 2"
    assert data["description"] == "Description 2"

def test_assign_user_to_project(client: TestClient):
    # Tạo user mới
    response = client.post(
        "/users/", json={"name": "Existing User", "email": "existing.email@example.com"}
    )
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Tạo project mới
    response = client.post(
        "/projects/", json={"name": "Project 1", "description": "Description 1"}
    )

    assert response.status_code == 201
    project_id = response.json()["id"]

    # Gán user vào project
    payload = {
        "user_id": user_id,
        "role": "manager"
    }
    
    response = client.post(f"/projects/{project_id}/assign_user", json = payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == f"User {user_id} successfully assigned to project {project_id}"


