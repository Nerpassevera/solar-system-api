from werkzeug.exceptions import HTTPException
from app.routes.route_utilities import validate_model
import pytest
from app.models.planet import Planet
...

def test_validate_Planet(two_saved_planets):
    # Act
    result_Planet = validate_model(Planet, 1)

    # Assert
    assert result_Planet.name == "Mercury"
    assert result_Planet.radius_in_mi == 1.516
    assert result_Planet.description == "about 1/3 the size of Earth"

def test_validate_Planet_missing_record(two_saved_planets):
    # Act & Assert
    # Calling `validate_Planet` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_Planet = validate_model(Planet, "3")
    
def test_validate_Planet_invalid_id(two_saved_planets):
    # Act & Assert
    # Calling `validate_Planet` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_Planet = validate_model(Planet, "cat")

