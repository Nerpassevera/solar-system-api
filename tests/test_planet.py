from app.models.planet import Planet
from pytest import raises

def test_planet_from_dict_creates_planet_instance():
    # Arrange
    planet_data = {
        "name": "Test Planet",
        "description": "This planet doesn't really exist",
        "radius_in_mi": 0
    }

    # Act
    new_planet = Planet.from_dict(planet_data)

    # Assert
    assert isinstance(new_planet, Planet)
    assert new_planet.name == "Test Planet"
    assert new_planet.description == "This planet doesn't really exist"
    assert new_planet.radius_in_mi == 0

def test_planet_from_dict_throws_exception_no_name():
    # Arrange
    planet_data = {
        "description": "This planet doesn't really exist",
        "radius in miles": 0
    }

    # Act & Assert
    with raises(KeyError):
        Planet.from_dict(planet_data)

def test_planet_from_dict_throws_exception_no_description():
    # Arrange
    planet_data = {
        "name": "Earth",
        "radius in miles": 0
    }

    # Act & Assert
    with raises(KeyError):
        Planet.from_dict(planet_data)

def test_planet_from_dict_throws_exception_no_radius_in_mi():
    # Arrange
    planet_data = {
        "name": "Earth",
        "description": "This planet doesn't really exist"
    }

    # Act & Assert
    with raises(KeyError):
        Planet.from_dict(planet_data)

def test_planet_from_dict_throws_exception_empty_data():
    # Arrange
    planet_data = {}

    # Act & Assert
    with raises(KeyError):
        Planet.from_dict(planet_data)

def test_from_dict_creates_planet_instance_with_extra_keys():
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "Earth",
        "description": "Earth, human population ~8.2 billions",
        "radius_in_mi" : 3.959,
        "another": "last value"
    }

    # Act
    new_planet = Planet.from_dict(test_data)

    # Arrange
    assert isinstance(new_planet, Planet)
    assert new_planet.name == "Earth"
    assert new_planet.description == "Earth, human population ~8.2 billions"

def test_planet_to_dict_no_missing_data():
    # Arrange
    test_data = Planet(
        id = 1,
        name = "Test Planet",
        description = "This planet doesn't really exist",
        radius_in_mi = 0
    )

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] == 1
    assert result["name"] == "Test Planet"
    assert result["description"] == "This planet doesn't really exist"
    assert result["radius_in_mi"] == 0

def test_planet_to_dict_missing_id():
    # Arrange
    test_data = Planet(
        name = "Test Planet",
        description = "This planet doesn't really exist",
        radius_in_mi = 0
    )

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] is None
    assert result["name"] == "Test Planet"
    assert result["description"] == "This planet doesn't really exist"
    assert result["radius_in_mi"] == 0
