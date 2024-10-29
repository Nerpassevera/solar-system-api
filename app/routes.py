from flask import Blueprint, make_response, abort, request, Response
from app.models.planet import Planet
from .db import db

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")

@planet_bp.post("/", strict_slashes=False)
def add_planet():
    request_body = request.get_json()
    name = request_body["name"],
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

@planet_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return planet.to_dict()

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        response = {"message": f"Planet ID {planet_id} is invalid."}
        abort(make_response(response, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)

    if not planet:
        response = {"message": f"Planet with ID {planet_id} not found."}
        abort(make_response(response, 404))

    return planet

@planet_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.radius_in_mi = request_body["radius_in_mi"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@planet_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")