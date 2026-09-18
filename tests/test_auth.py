from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_activities_are_publicly_accessible():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_sign_up_requires_admin_authentication():
    email = f"student-{uuid4()}@mergington.edu"

    response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


def test_valid_admin_credentials_can_register_student():
    email = f"admin-student-{uuid4()}@mergington.edu"

    response = client.post(
        f"/activities/Chess Club/signup?email={email}",
        auth=("teacher", "admin123"),
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_invalid_admin_credentials_are_rejected():
    email = f"bad-admin-{uuid4()}@mergington.edu"

    response = client.post(
        f"/activities/Chess Club/signup?email={email}",
        auth=("teacher", "wrong-password"),
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"
