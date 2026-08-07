#!/usr/bin/python3
"""SQLAlchemy Place model."""

from app import db
from app.models.basemodel import BaseModel


place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Represent a place in the database."""

    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(self, title, description, price, latitude, longitude, user_id, **kwargs):
        """Initialize a place."""
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id
