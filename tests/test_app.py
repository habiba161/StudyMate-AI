import os
import sys
import tempfile
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, init_db

@pytest.fixture
def client():
    db_fd, test_db_path = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config["DATABASE"] = test_db_path

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(test_db_path)

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"StudyMate AI" in response.data

def test_post_topic_returns_response(client):
    response = client.post("/", data={"topic": "Database"})
    assert response.status_code == 200
    assert b"AI Explanation for: Database" in response.data

def test_history_is_saved(client):
    client.post("/", data={"topic": "Python"})
    response = client.get("/")
    assert b"Python" in response.data

def test_multiple_topics_saved(client):
    client.post("/", data={"topic": "AI"})
    client.post("/", data={"topic": "Flask"})
    response = client.get("/")
    assert b"AI" in response.data
    assert b"Flask" in response.data