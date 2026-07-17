from app.models.basemodel import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def __str__(self):
        return f"Review({self.rating}/5: {self.text})"
