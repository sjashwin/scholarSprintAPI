from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

def test_create_room():
    response = client.post("/create-room")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 

    # Use an instance of your Question model to get the keys
    question_keys = ["q", "a", "d", "w", "s", "c"]

    for question in response.json():
        assert all(key in question for key in question_keys)