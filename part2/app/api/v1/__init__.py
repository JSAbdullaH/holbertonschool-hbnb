#!/usr/bin/python3
"""Version 1 API package."""

from flask_restx import Api
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

api = Api(
    version="1.0",
    title="HBnB API",
    description="HBnB application API"
)

api.add_namespace(places_ns, path="/places")
api.add_namespace(reviews_ns, path="/reviews")
