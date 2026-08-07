#!/usr/bin/python3
"""SQLAlchemy Review model."""

from app import db
from app.models.basemodel import BaseModel


class Review(BaseModel):
    """Represent a review in the database."""

    __tablename__ = "reviews"

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, text, rating, **kwargs):
        """Initialize a review."""
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
