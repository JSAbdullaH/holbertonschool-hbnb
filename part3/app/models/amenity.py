from app.models.basemodel import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("name is required (max 50 chars)")
        self.name = name

    def __str__(self):
        return f"Amenity({self.name})"
