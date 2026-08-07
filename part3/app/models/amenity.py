#!/usr/bin/python3
"""SQLAlchemy Amenity model."""

from app import db
from app.models.basemodel import BaseModel


class Amenity(BaseModel):
    """Represent an amenity in the database."""

    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name, **kwargs):
        """Initialize an amenity."""
        super().__init__(**kwargs)
        self.name = name
