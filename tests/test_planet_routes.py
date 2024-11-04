def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_planet_with_no_records(client):
    # Act
    response = client.get("/planets/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet with ID 2 not found."}

def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "name": "Venus",
        "description": "only slightly smaller than Earth",
        "radius_in_mi": 3.760
    }

def test_create_one_book(client):
    # Act
    response = client.post("/planets", json={
        "name": "Earth",
        "description": "Earth itself",
        "radius_in_mi" : 3.959
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Earth",
        "description": "Earth itself",
        "radius_in_mi" : 3.959
    }