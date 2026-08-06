#!/usr/bin/python3
"""Repository interfaces and implementations."""

from abc import ABC, abstractmethod

from app import db


class Repository(ABC):
    """Abstract repository interface."""

    @abstractmethod
    def add(self, obj):
        """Add an object."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Get an object by ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Get all objects."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by an attribute."""
        pass


class InMemoryRepository(Repository):
    """Repository using in-memory storage."""

    def __init__(self):
        """Initialize empty storage."""
        self._storage = {}

    def add(self, obj):
        """Add an object to storage."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Get an object by ID."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Return all stored objects."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update a stored object."""
        obj = self.get(obj_id)

        if obj:
            for key, value in data.items():
                setattr(obj, key, value)

        return obj

    def delete(self, obj_id):
        """Delete an object from storage."""
        return self._storage.pop(obj_id, None)

    def get_by_attribute(self, attr_name, attr_value):
        """Return an object matching an attribute."""
        return next(
            (
                obj
                for obj in self._storage.values()
                if getattr(obj, attr_name, None) == attr_value
            ),
            None,
        )


class SQLAlchemyRepository(Repository):
    """Generic repository using SQLAlchemy."""

    def __init__(self, model):
        """Initialize the repository with a model class."""
        self.model = model

    def add(self, obj):
        """Add an object to the database."""
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Get an object by ID."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Return all objects."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object in the database."""
        obj = self.get(obj_id)

        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete an object from the database."""
        obj = self.get(obj_id)

        if not obj:
            return None

        db.session.delete(obj)
        db.session.commit()
        return obj

    def get_by_attribute(self, attr_name, attr_value):
        """Return the first object matching an attribute."""
        return self.model.query.filter_by(
            **{attr_name: attr_value}
        ).first()
