import re
from app.models.basemodel import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required (max 50 chars)")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required (max 50 chars)")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def __str__(self):
        return f"User({self.first_name} {self.last_name}, {self.email})"
