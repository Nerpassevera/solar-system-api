from sqlalchemy.orm import Mapped, mapped_column
from app.db import db
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    radius_in_mi: Mapped[float]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "radius_in_mi": self.radius_in_mi
        }
    
    @classmethod
    def from_dict(cls, planet_data):
        return Planet(
            name = planet_data["name"],
            description = planet_data["description"],
            radius_in_mi = planet_data["radius_in_mi"]
        )

# planets_dicts = [
    # {
    #     "id": 1, "name": "Mercury",
    #         "radius_in_mi": 1.516,
    #         "description": "about 1/3 the size of Earth"
    #     },
    # {
    #     "id": 2,
    #     "name" : "Venus",
    #     "radius_in_mi" : 3.760,
    #     "description":  "only slightly smaller than Earth"
    # },
    # {
    #     "id": 3,
    #     "name" : "Earth",
    #     "radius_in_mi" : 3.959,
    #     "description": "Earth itself"
    # },
    # {
    #     "id": 4,
    #     "name" : "Mars",
    #     "radius_in_mi" : 2.106,
    #     "description":  "about half the size of Earth"
    # },
    # {
    #     "id": 5,
    #     "name" : "Jupiter",
    #     "radius_in_mi" : 43.441,
    #     "description": "11x Earth’s size"
    # },
    # {
    #     "id": 6,
    #     "name" : "Saturn",
    #     "radius_in_mi" : 36.184,
    #     "description": "9x larger than Earth"
    # },
    # {
    #     "id": 7,
    #     "name" : "Uranus",
    #     "radius_in_mi" : 15.759,
    #     "description":  "4x Earth’s size"
    # },
    # {
    #     "id": 8,
    #     "name" : "Neptune",
    #     "radius_in_mi" : 15.299,
    #     "description": "only slightly smaller than Uranus"
    # }
#     ]
