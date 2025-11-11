import pytest
from feladat_1.app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    """Test the root endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_get_todos(client):
    """Test fetching all to-do items from the database."""
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.is_json
    # We added 2 items in the fixture, so we expect to get them back
    assert len(response.json) == 2

def test_add_todo(client):
    """Test adding a new todo item via POST."""
    payload = {"task": "Finish the project"}
    response = client.post('/todos', json=payload)

    assert response.status_code == 201
    assert response.is_json
    assert response.json["task"] == "Finish the project"
    assert response.json["done"] is False

    # Ellenőrizzük hogy nőtt a lista mérete
    response2 = client.get('/todos')
    assert len(response2.json) == 3