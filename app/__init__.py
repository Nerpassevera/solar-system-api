from flask import Flask
from .db import db, migrate

from app.routes.planet_routes import planet_bp
from app.routes.moon_routes import bp as moon_bp
from .models.planet import Planet
from .models.moon import Moon
from os import environ


def create_app(config=None):

    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(planet_bp)
    app.register_blueprint(moon_bp)

    return app
