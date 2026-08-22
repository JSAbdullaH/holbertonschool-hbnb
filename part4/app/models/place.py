from app.models.basemodel import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("title is required (max 100 chars)")
        if price is None or float(price) <= 0:
            raise ValueError("price must be a positive value")
        if latitude is None or not -90.0 <= float(latitude) <= 90.0:
            raise ValueError("latitude must be between -90 and 90")
        if longitude is None or not -180.0 <= float(longitude) <= 180.0:
            raise ValueError("longitude must be between -180 and 180")
        if not isinstance(owner, User):
            raise ValueError("owner must be a valid User instance")
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def __str__(self):
        return f"Place({self.title}, {self.price})"
