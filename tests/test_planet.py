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