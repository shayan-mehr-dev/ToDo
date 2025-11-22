import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_todo_simple():
    response = client.post("/todos", json={"title": "Test Task 1", "description": "This is a simple test"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Task 1"
    assert data["description"] == "This is a simple test"


def test_get_todos_list():
    # I must be confident that list is not empty
    client.post("/todos", json={"title": "Sample Task for GET", "description": "Test description"})
    
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # at least 1 task must exist
    assert any("title" in item and "description" in item for item in data)



@pytest.fixture
def create_task():
    response = client.post("/todos", json={"title": "Sample Task", "description": "Sample description"})
    data = response.json()
    yield data["id"]
    # I don't delet test for avoid interference with delete testing
    # client.delete(f"/todos/{data['id']}")



def test_delete_todo_task(create_task):
    todo_id = create_task
    # deleting task
    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 200
    
    # checking do it really has deleted?
    get_response = client.get("/todos")
    ids = [t["id"] for t in get_response.json()]
    assert todo_id not in ids


def test_delete_nonexistent_todo():
    response = client.delete("/todos/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Todo not found"


def test_create_todo_invalid():
    # without title
    response = client.post("/todos", json={"description": "Missing title"})
    assert response.status_code == 422


def test_create_todo():
    response = client.post("/todos", json={"title": "Test Task", "description": "This is a test"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test"

def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_todo(create_task):
    todo_id = create_task
    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 200
    
    get_response = client.get("/todos")
    ids = [t["id"] for t in get_response.json()]
    assert todo_id not in ids
