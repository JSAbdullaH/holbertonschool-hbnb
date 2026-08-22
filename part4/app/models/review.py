from app.models.basemodel import BaseModel
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not text:
            raise ValueError("text is required")
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("rating must be an integer between 1 and 5")
        if place is None or not hasattr(place, "add_review"):
            raise ValueError("place must be a valid Place instance")
        if not isinstance(user, User):
            raise ValueError("user must be a valid User instance")
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def __str__(self):
        return f"Review({self.rating}/5: {self.text})"
