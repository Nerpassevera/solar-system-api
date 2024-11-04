from flask import abort, make_response
from ..db import db
from app.models.planet import Planet

def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} with ID {model_id} not found."}
        abort(make_response(response, 404))

    return model

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