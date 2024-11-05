from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .planet import Planet

class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    size: Mapped[float]
    description: Mapped[str]
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="planets")

    def to_dict(self):
        moon_as_dict = {}
        moon_as_dict["id"] = self.id
        moon_as_dict["size"] = self.size
        moon_as_dict["description"] = self.description

        if self.planet:
            moon_as_dict["planet"] = self.planet.name

        return moon_as_dict
    
    @classmethod
    def from_dict(cls, moon_data):
        # Use get() to fetch values that could be undefined to avoid raising an error
        planet_id = moon_data.get("planet_id")

        new_moon = cls(
            size=moon_data["size"],
            description=moon_data["description"],
            planet_id=planet_id
        )
