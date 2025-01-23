from .conftest import TestClient
from uuid import UUID

def test_create_users(client: TestClient):
    response = client.post(
        "/users/", json={"name": "Deadpond", "email": "duytien@gmail.com"}
    )
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Deadpond"
    assert data["email"] == "duytien@gmail.com"

def test_update_users(client: TestClient):
    # Tạo người dùng mới để đảm bảo user_id tồn tại
    response = client.post(
        "/users/", json={"name": "Existing User", "email": "existing.email@example.com"}
    )
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Cập nhật thông tin người dùng
    updated_data = {
        "name": "New",
        "email": "new.email@example.com"
    }
    response = client.patch(f"/users/{user_id}", json=updated_data)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "New"
    assert data["email"] == "new.email@example.com"

def test_delete_users(client: TestClient):
    # Tạo người dùng mới để đảm bảo user_id tồn tại
    response = client.post(
        "/users/", json={"name": "Existing User", "email": "existing.email@example.com"}
    )
    assert response.status_code == 201
    user_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

def test_get_user_projects(client: TestClient):
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

    # lấy info dựa avo2 user_id
    response = client.get(f"/users/{user_id}/projects")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == user_id
    assert data["name"] == "Existing User"
    assert data["email"] == "existing.email@example.com"
    assert len(data["projects"]) == 1
    assert data["projects"][0]["project_id"] == project_id
    assert data["projects"][0]["project_name"] == "Project 1"
    assert data["projects"][0]["role"] == "manager"
# "id": user.id,
# "name": user.name,
# "email": user.email,
# "projects": projects_and_roles