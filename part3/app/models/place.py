#!/usr/bin/python3
"""SQLAlchemy Place model."""

from app import db
from app.models.basemodel import BaseModel


class Place(BaseModel):
    """Represent a place in the database."""

    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    def __init__(self, title, description, price, latitude, longitude, **kwargs):
        """Initialize a place."""
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
