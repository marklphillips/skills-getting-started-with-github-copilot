"""Tests for FastAPI endpoints."""


def test_get_activities(client, sample_activities):
    """Test GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 2
    assert "Chess Club" in data
    assert "Programming Class" in data

    # Check structure of one activity
    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_signup_success(client):
    """Test successful signup for an activity."""
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]

    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate(client):
    """Test signup fails when student is already signed up."""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    # Second signup should fail
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student is already signed up for this activity" in data["detail"]


def test_signup_activity_not_found(client):
    """Test signup fails for non-existent activity."""
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_remove_participant_success(client):
    """Test successful removal of a participant."""
    # First add a participant
    client.post("/activities/Programming%20Class/signup?email=toremove@mergington.edu")

    # Now remove them
    response = client.delete("/activities/Programming%20Class/participants?email=toremove@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Removed toremove@mergington.edu from Programming Class" in data["message"]

    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "toremove@mergington.edu" not in activities["Programming Class"]["participants"]


def test_remove_participant_not_found(client):
    """Test removal fails when participant is not signed up."""
    response = client.delete("/activities/Chess%20Club/participants?email=notsignedup@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]


def test_remove_participant_activity_not_found(client):
    """Test removal fails for non-existent activity."""
    response = client.delete("/activities/NonExistent/participants?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]