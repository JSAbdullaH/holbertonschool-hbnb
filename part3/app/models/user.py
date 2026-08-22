#!/usr/bin/python3
"""SQLAlchemy User model."""

import re

from app import bcrypt, db
from app.models.basemodel import BaseModel


class User(BaseModel):
    """Represent an application user."""

    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    places = db.relationship('Place', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password=None,
        is_admin=False
    ):
        """Initialize a user."""
        if not first_name or len(first_name) > 50:
            raise ValueError(
                "first_name is required (max 50 chars)"
            )

        if not last_name or len(last_name) > 50:
            raise ValueError(
                "last_name is required (max 50 chars)"
            )

        if (
            not email
            or not re.match(r"[^@]+@[^@]+\.[^@]+", email)
        ):
            raise ValueError("Invalid email format")

        if not password:
            raise ValueError("Password is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, password):
        """Hash a plaintext password."""
        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def verify_password(self, password):
        """Verify a plaintext password."""
        return bcrypt.check_password_hash(
            self.password,
            password
        )

    def __str__(self):
        """Return a readable user representation."""
        return "User({} {}, {})".format(
            self.first_name,
            self.last_name,
            self.email
        )
