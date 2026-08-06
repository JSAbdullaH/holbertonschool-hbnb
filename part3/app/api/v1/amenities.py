#!/usr/bin/python3
"""Amenity API endpoints with administrator access control."""

from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace("amenities", description="Amenity operations")


amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(
            required=True,
            description="Name of the amenity"
        )
    },
)


def amenity_to_dict(amenity):
    """Convert an Amenity object to a dictionary."""
    return {
        "id": amenity.id,
        "name": amenity.name,
    }


@api.route("/")
class AmenityList(Resource):
    """Handle operations on the amenities collection."""

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Missing or invalid token")
    @api.response(403, "Administrator privileges required")
    @jwt_required()
    def post(self):
        """Allow an administrator to create an amenity."""
        claims = get_jwt()

        if not claims.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        amenity_data = (api.payload or {}).copy()

        try:
            new_amenity = facade.create_amenity(amenity_data)
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        return amenity_to_dict(new_amenity), 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Return all amenities publicly."""
        amenities = facade.get_all_amenities()

        return [
            amenity_to_dict(amenity)
            for amenity in amenities
        ], 200


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    """Handle operations on a specific amenity."""

    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Return an amenity by ID."""
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity_to_dict(amenity), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(401, "Missing or invalid token")
    @api.response(403, "Administrator privileges required")
    @api.response(404, "Amenity not found")
    @jwt_required()
    def put(self, amenity_id):
        """Allow an administrator to update an amenity."""
        claims = get_jwt()

        if not claims.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        amenity_data = (api.payload or {}).copy()

        try:
            updated_amenity = facade.update_amenity(
                amenity_id,
                amenity_data
            )
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        if not updated_amenity:
            updated_amenity = facade.get_amenity(amenity_id)

        return amenity_to_dict(updated_amenity), 200
