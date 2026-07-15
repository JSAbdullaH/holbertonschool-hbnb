#models For users
from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, username, firstname, lastname, email, password):
        super().__init__()
        self.id = self.generate_id()
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        is_admin = False
        self.created_at = self.get_current_time()
        self.updated_at = self.get_current_time()

    def __str__(self):
        return f"User(username={self.username}, email={self.email})"

