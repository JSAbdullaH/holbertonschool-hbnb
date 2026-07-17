import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = self.generate_id()
        self.created_at = self.get_current_time()
        self.updated_at = self.get_current_time()

    def generate_id(self):
        return str(uuid.uuid4())

    def get_current_time(self):
        return datetime.now()

    def save(self):
        self.updated_at = self.get_current_time()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
