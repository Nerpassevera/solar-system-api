from flask import Blueprint, make_response, abort
from app.models.planet import planets

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")

@planet_bp.get("")
def get_all_planets():
    return [planet.to_dict() for planet in planets]

@planet_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return planet.to_dict()

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        response = {"messange" : f"planet id {planet_id} is invalid"}
        abort(make_response(response, 400))

    for planet in planets:
        if planet.id == planet_id:
            return planet
    
    response = {"messange" : f"planet with id {planet_id} not found"}
    abort(make_response(response, 404))