import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    test_email = "testuser@mergington.edu"
    activity = "Art Club"

    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": test_email})

    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 200
    assert f"Signed up {test_email} for {activity}" in response.json()["message"]

    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response.status_code == 200
    assert f"Unregistered {test_email} from {activity}" in response.json()["message"]

    # Try unregistering again (should fail)
    response = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/NonexistentActivity/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_activity_not_found():
    response = client.delete("/activities/NonexistentActivity/unregister", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

