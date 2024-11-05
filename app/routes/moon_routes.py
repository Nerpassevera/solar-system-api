from flask import Blueprint, request, make_response, abort
from app.models.moon import Moon
from ..db import db

bp = Blueprint("moon_bp", __name__, url_prefix="/moons")