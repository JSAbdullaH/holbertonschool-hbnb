#!/usr/bin/python3
"""Amenity model."""

from app.models.basemodel import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def __str__(self):
        return (
            f"Amenity(name={self.name}, "
            f"description={self.description})"
        )

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "name": self.name,
            "description": self.description
        })
        return data