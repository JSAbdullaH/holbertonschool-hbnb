#Models For amenity
from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        self.id = self.generate_id()
        self.name = name
        self.description = description
        self.created_at = self.get_current_time()
        self.updated_at = self.get_current_time()

    def __str__(self):
        return f"Amenity(name={self.name}, description={self.description})"