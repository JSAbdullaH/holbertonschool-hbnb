#!/usr/bin/python3
"""Repository dedicated to User database operations."""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Provide database operations for User objects."""

    def __init__(self):
        """Initialize the user repository."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """Return a user matching the supplied email."""
        return self.get_by_attribute("email", email)
