#Models For Reviews
from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, user_id, place_id, rating, comment):
        super().__init__()
        self.id = self.generate_id()
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
        self.created_at = self.get_current_time()
        self.updated_at = self.get_current_time()

    def __str__(self):
        return f"Review(user_id={self.user_id}, place_id={self.place_id}, rating={self.rating})"