from flask import Blueprint
from app.models.planet import planets

planet_bp = Blueprint("planet_bp", __name__, url_prefix="/planets")

@planet_bp.get("")
def get_all_planets():
    return [planet.to_dict() for planet in planets]
