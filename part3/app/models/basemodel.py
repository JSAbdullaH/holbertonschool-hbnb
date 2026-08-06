#!/usr/bin/python3
"""Base model for all SQLAlchemy entities."""

import uuid
from datetime import datetime

from app import db


class BaseModel(db.Model):
    """Base SQLAlchemy model."""

    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def save(self):
        """Update the modification time."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update allowed object attributes."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()

    def to_dict(self):
        """Return a dictionary representation."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
            "updated_at": self.updated_at.isoformat()
            if self.updated_at else None,
        }
