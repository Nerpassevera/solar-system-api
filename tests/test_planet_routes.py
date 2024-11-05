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

def test_create_one_planet(client):
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


def test_create_one_planet_no_name(client):
    # Arrange
    test_data = {
        "description": "Earth itself",
        "radius_in_mi" : 3.959
    }

    # Act
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == { "message": "ERROR: Missing the name parameter for creating a planet" }

def test_create_one_planet_no_description(client):
    # Arrange
    test_data = {
        "name": "Earth",
        "radius_in_mi" : 3.959
    }

    # Act
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == { "message": "ERROR: Missing the description parameter for creating a planet" }

def test_create_one_planet_with_extra_key(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "Earth",
        "description": "Earth itself",
        "radius_in_mi" : 3.959,
        "another": "last value"
    }

    # Act
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Earth",
        "description": "Earth itself",
        "radius_in_mi" : 3.959,
    }

def test_create_planet_with_no_params(client):
    # Arrange
    test_data = {}

    # Act
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == { "message": "ERROR: No parameters for planet has been passed!" }

def test_delete_planet_deletes_planet(client, two_saved_planets):
    # Arrange
    planet1 = {
        "id": 1,
        "name": "Earth",
        "description": "Earth itself",
        "radius_in_mi" : 3.959
        }
    
    # Act
    
    response = client.delete("/planets/1")
    planets = client.get("/planets").get_json()

    # Assert
    assert planet1 not in planets
    assert response.status_code == 204

def test_delete_planet_does_not_delete_planet_if_no_id(client, two_saved_planets):
    # Arrange
    response = client.get("/planets")
    initial_planets = response.get_json()

    # Act
    response = client.delete("/planets/")
    planets = client.get("/planets").get_json()

    # Assert
    assert planets == initial_planets
    assert response.status_code == 405

def test_delete_planet_does_not_delete_planet_if_id_not_num(client, two_saved_planets):
    # Arrange
    response = client.get("/planets")
    initial_planets = response.get_json()

    # Act
    
    response = client.delete("/planets/one")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet one invalid"}

def test_edit_planet_updates_planet(client, two_saved_planets):
    # Arrange
    planet1_change = {
        "id": 1,
        "name": "Earth",
        "description": "Earth, human population ~8.2 billions",
        "radius_in_mi" : 3.959
        }

    # Act

    response = client.put("/planets/1", json=planet1_change)
    planet1 = client.get("/planets/1").get_json()

    # Assert
    assert response.status_code == 204
    assert planet1 == planet1_change

def test_edit_planet_updates_planet_with_extra_keys(client, two_saved_planets):
    # Arrange
    planet1_change = {
        "extra": "some stuff",
        "name": "Earth",
        "description": "Earth, human population ~8.2 billions",
        "radius_in_mi" : 3.959,
        "another": "last value"
        }
    expected_planet = {
        "id": 1,
        "name": "Earth",
        "description": "Earth, human population ~8.2 billions",
        "radius_in_mi" : 3.959
        }

    # Act
    response = client.put("/planets/1", json=planet1_change)
    planet1 = client.get("/planets/1").get_json()

    # Assert
    assert response.status_code == 204
    assert planet1 == expected_planet

def test_edit_a_planet_does_not_update_planet_with_no_id(client, two_saved_planets):
    # Arrange
    planet1_change = {
        "name": "Earth",
        "description": "Earth, human population ~8.2 billions",
        "radius_in_mi" : 3.959
        }

    # Act
    response = client.put("/planets/", json=planet1_change)
    planet1 = client.get("/planets/1").get_json()

    # Assert
    assert response.status_code == 405
    assert planet1 != planet1_change

def test_edit_planet_does_not_update_planet_with_non_num_id(client, two_saved_planets):
    # Arrange
    planet1_change = {
        "name": "Earth",
        "description": "Earth, human population ~8.2 billions",
        "radius_in_mi" : 3.959
        }

    # Act
    response = client.put("/planets/one", json=planet1_change)
    response_body = response.get_json()
    planet1 = client.get("/planets/1").get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet one invalid"}
    assert planet1 != planet1_change

def test_edit_planet_returns_message_if_id_not_found(client, two_saved_planets):
    # Arrange
    planet1_change = {
        "name": "Earth",
        "description": "Earth, human population ~8.2 billions",
        "radius_in_mi" : 3.959
        }

    # Act
    response = client.put("/planets/3", json=planet1_change)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == { "message": "Planet with ID 3 not found." }
