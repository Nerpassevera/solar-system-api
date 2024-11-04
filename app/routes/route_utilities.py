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
    new_planet = Planet.from_dict(request_body)
    db.session.add(new_planet)
    db.session.commit()

    return new_planet