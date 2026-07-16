#!/usr/bin/python3
"""Amenities API endpoints."""

from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace(
    "amenities",
    description="Operations related to amenities"
)

amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(
            required=True,
            description="Amenity name"
        ),
        "description": fields.String(
            required=True,
            description="Amenity description"
        )
    }
)

amenity_response = api.model(
    "AmenityResponse",
    {
        "id": fields.String,
        "name": fields.String,
        "description": fields.String
    }
)


def serialize_amenity(amenity):
    """Convert Amenity object to dictionary."""
    return {
        "id": amenity.id,
        "name": amenity.name,
        "description": amenity.description
    }


def validate_amenity_data(data, partial=False):
    """Validate amenity data."""

    if not data:
        return False, "No input data provided"

    required_fields = ["name", "description"]

    if not partial:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

    if "name" in data and not data["name"].strip():
        return False, "Amenity name cannot be empty"

    if "description" in data and not data["description"].strip():
        return False, "Amenity description cannot be empty"

    return True, None


@api.route("/")
class AmenityList(Resource):
    """Operations on amenities collection."""

    @api.marshal_list_with(amenity_response)
    def get(self):
        """Return all amenities."""
        amenities = facade.get_all_amenities()
        return [serialize_amenity(a) for a in amenities], 200

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_response, code=201)
    def post(self):
        """Create a new amenity."""

        data = request.get_json()

        valid, error = validate_amenity_data(data)

        if not valid:
            return {"error": error}, 400

        amenity = facade.create_amenity(
            name=data["name"],
            description=data["description"]
        )

        return serialize_amenity(amenity), 201


@api.route("/<string:amenity_id>")
@api.param("amenity_id", "Amenity ID")
class Amenity(Resource):
    """Operations on a single amenity."""

    @api.marshal_with(amenity_response)
    def get(self, amenity_id):
        """Return one amenity."""

        amenity = facade.get_amenity(amenity_id)

        if amenity is None:
            return {"error": "Amenity not found"}, 404

        return serialize_amenity(amenity), 200

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_response)
    def put(self, amenity_id):
        """Update an amenity."""

        amenity = facade.get_amenity(amenity_id)

        if amenity is None:
            return {"error": "Amenity not found"}, 404

        data = request.get_json()

        valid, error = validate_amenity_data(data, partial=True)

        if not valid:
            return {"error": error}, 400

        updated_amenity = facade.update_amenity(
            amenity_id,
            data
        )

        return serialize_amenity(updated_amenity), 200