from app.models.basemodel import BaseModel


class Place(BaseModel):
    def __init__(self, name, description, location, price_range, owner):
        super().__init__()

        self.name = name
        self.description = description
        self.location = location
        self.price_range = price_range
        self.owner = owner

    def __str__(self):
        return f"Place(name={self.name}, location={self.location})"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "price_range": self.price_range,
            "owner": self.owner
        })
        return data