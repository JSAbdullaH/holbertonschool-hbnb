#Models For places
from app.models.basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, name, description, location, price_range):
        super().__init__()
        self.id = self.generate_id()
        self.name = name
        self.description = description
        self.location = location
        self.price_range = price_range
        self.owner = owner
        self.created_at = self.get_current_time()
        self.updated_at = self.get_current_time()

    def __str__(self):
        return f"Place(name={self.name}, location={self.location})"
