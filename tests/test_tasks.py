from .conftest import TestClient
from uuid import UUID
import json
def create_info(client: TestClient):
    response = client.post(
        "/projects/", json={"name": "Project 1", "description": "Description 1"}
    )
    assert response.status_code == 201
    project_id = response.json()["id"]
    # tạo status
    response = client.post(
        "/status/", json={"status": "Good"}
    )
    assert response.status_code == 201
    status_id = response.json()["id"]
    # tạo user
    response = client.post(
        "/users/", json={"name": "User 1", "email": "duytien@gmail.com"})
    assert response.status_code == 201
    user_id = response.json()["id"]
    return project_id, status_id, user_id

def test_create_task(client: TestClient):
    project_id, status_id, user_id = create_info(client)
    response = client.post(
        "/task/", json={
                        "name": "Task 1", 
                        "description": "Description 1",  
                        "deadline": "2025-01-26T03:45:52.299Z",
                        "project_id": project_id,
                        "status_id": status_id,
                        "user_id": user_id
                        }                        
    )
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Task 1"
    assert data["description"] == "Description 1"

def test_get_tasks(client: TestClient):
    project_id, status_id, user_id = create_info(client)
    response = client.post(
        "/task/", json={
                        "name": "Task 1", 
                        "description": "Description 1",  
                        "deadline": "2025-01-26T03:45:52.299Z",
                        "project_id": project_id,
                        "status_id": status_id,
                        "user_id": user_id
                        }                        
    )
    assert response.status_code == 201

    response = client.get("/task/?offset=0&limit=100")
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0

def test_delete_task(client: TestClient):
    project_id, status_id, user_id = create_info(client)
    response = client.post(
        "/task/", json={
                        "name": "Task 1", 
                        "description": "Description 1",  
                        "deadline": "2025-01-26T03:45:52.299Z",
                        "project_id": project_id,
                        "status_id": status_id,
                        "user_id": user_id
                        }                        
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.delete(
        "/task/?task_ids=" + str(task_id),
    )
    assert response.status_code == 200

def test_update_task(client: TestClient):
    project_id, status_id, user_id = create_info(client)
    response = client.post(
        "/task/", json={
                        "name": "Task 1", 
                        "description": "Description 1",  
                        "deadline": "2025-01-26T03:45:52.299Z",
                        "project_id": project_id,
                        "status_id": status_id,
                        "user_id": user_id
                        }                        
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    # tạo status mới
    response = client.post("/status/", json={"status": "Bad"})
    assert response.status_code == 201
    status_id = response.json()["id"]

    updated_data = {
        "name": "Task 2",
        "description": "Description 2",
        "status_id": status_id
    }
    response = client.patch(f"/task/{task_id}", json=updated_data)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Task 2"
    assert data["description"] == "Description 2"
    assert data["status_id"] == status_id

def test_allocate_task_user(client: TestClient):
    project_id, status_id, user_id = create_info(client)
    response = client.post(
        "/task/", json={
                        "name": "Task 1", 
                        "description": "Description 1",  
                        "deadline": "2025-01-26T03:45:52.299Z",
                        "project_id": project_id,
                        "status_id": status_id,
                        "user_id": user_id
                        }                        
    )
    assert response.status_code == 201
    task_id = response.json()["id"]
    # tạo user mới
    response = client.post(
        "/users/", json={"name": "User 2", "email": "duy@gmail.com"})
    assert response.status_code == 201
    user_id = response.json()["id"]

    response = client.patch(f"/task/{task_id}/assign_user", json={"user_id": user_id})
    data = response.json()
    assert response.status_code == 200
    assert data["user_id"] == user_id
    assert data["id"] == task_id