#!/usr/bin/python3
"""SQLAlchemy Review model."""

from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Review model mapped to the reviews table."""
    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
