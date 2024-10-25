from flask import Blueprint, make_response, abort, request
from app.models.planet import Planet
from .db import db

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")

@planet_bp.post("/", strict_slashes=False)
def add_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    radius_in_mi = request_body["radius_in_mi"]

    new_planet = Planet(
        name=name,
        description=description,
        radius_in_mi=radius_in_mi
    )
    db.session.add(new_planet)
    db.session.commit()

    return new_planet.to_dict(), 201

@planet_bp.get("")
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)
    return [ planet.to_dict() for planet in planets]