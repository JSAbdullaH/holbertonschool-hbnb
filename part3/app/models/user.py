import re
from app.models.basemodel import BaseModel
from app import bcrypt


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
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
        self.password = None
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify a plaintext password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    def __str__(self):
        return f"User({self.first_name} {self.last_name}, {self.email})"