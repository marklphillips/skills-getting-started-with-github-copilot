import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """TestClient fixture for FastAPI app testing."""
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """Sample activities data for testing."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        }
    }


@pytest.fixture(autouse=True)
def reset_activities(sample_activities):
    """Reset global activities dict before each test."""
    global activities
    activities.clear()
    activities.update(sample_activities)