from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_quiz():
    response = client.get("/quiz")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Manually define the keys based on your Quiz model
    quiz_keys = ["_id", "time", "image", "size", "type", "name"]

    for quiz in response.json():
        assert all(key in quiz for key in quiz_keys)