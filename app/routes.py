from flask import Blueprint, make_response, abort, request, Response
from app.models.planet import Planet
from .db import db

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")

@planet_bp.post("/", strict_slashes=False)
def add_planet():
    request_body = request.get_json()
    created_planet = create_planet_helper(request_body)

    return created_planet.to_dict(), 201

def create_planet_helper(request_body):
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

    return new_planet

@planet_bp.get("/", strict_slashes=False)
def get_all_planets():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)
    return [ planet.to_dict() for planet in planets]

@planet_bp.get("/<planet_id>", strict_slashes=False)
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

@planet_bp.put("/<planet_id>", strict_slashes=False)
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.radius_in_mi = request_body["radius_in_mi"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@planet_bp.delete("/<planet_id>", strict_slashes=False)
def delete_planet(planet_id):
    planet = validate_planet(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@planet_bp.post("/import/", strict_slashes=False)
def create_multiple_planets():
    request_body = request.get_json()
    for planet_data in request_body["planets"]:
        create_planet_helper(planet_data)

    return Response(status=201, response="Planets have been created!", mimetype="application/json")

@planet_bp.delete("/delete_all/", strict_slashes=False)
def delete_all_planets():
    num_rows_deleted = db.session.query(Planet).delete()
    db.session.commit()

    return Response(status=200, response=f"All {num_rows_deleted} planets have been deleted!", mimetype="application/json")