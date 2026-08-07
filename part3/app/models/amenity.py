#!/usr/bin/python3
"""SQLAlchemy Amenity model."""

from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity model mapped to the amenities table."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(128), nullable=False)
