from flask import Blueprint, make_response, abort, request, Response
from app.models.planet import Planet

from ..db import db
from app.routes.route_utilities import validate_model, create_planet_helper

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")

@planet_bp.post("/", strict_slashes=False)
def add_planet():
    request_body = request.get_json()
    created_planet = create_planet_helper(request_body)

    return created_planet.to_dict(), 201

def create_planet_helper(request_body):
    new_planet = Planet.from_dict(request_body)
    db.session.add(new_planet)
    db.session.commit()

    return new_planet

@planet_bp.get("/", strict_slashes=False)
def get_all_planets():
    query = db.select(Planet)

    # Description filter
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    # Radius in miles filter
    radius_param = request.args.get("radius_in_mi")
    if radius_param:
        try:
            radius_param = int(radius_param)
        except ValueError:
            return []
        query = query.where(Planet.radius_param < radius_param)

    allowed_sort_fields = {
        "name": Planet.name,
        "radius_in_mi": Planet.radius_in_mi,
    }

    sort_param = request.args.get("sort")
    if sort_param:
        sort_param = sort_param.split(" ")
        # Selects the field for sorting based on the user's input (`sort_param[0]`).
        # If no valid sort field is specified, defaults to sorting by Planet.id.
        sort_field = allowed_sort_fields.get(sort_param[0].lower(), Planet.id)

        if sort_param[-1] == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field)

    planets = db.session.scalars(query)

    return [ planet.to_dict() for planet in planets]

@planet_bp.get("/<planet_id>", strict_slashes=False)
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return planet.to_dict()


@planet_bp.put("/<planet_id>", strict_slashes=False)
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.radius_in_mi = request_body["radius_in_mi"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@planet_bp.delete("/<planet_id>", strict_slashes=False)
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
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

    return Response(
        status=200,
        response=f"All {num_rows_deleted} planets have been deleted!",
        mimetype="application/json")
