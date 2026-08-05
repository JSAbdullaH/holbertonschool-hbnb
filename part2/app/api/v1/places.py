#!/usr/bin/python3
"""Place API endpoints with authentication and admin access control."""

from flask import request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace("places", description="Place operations")


place_model = api.model(
    "Place",
    {
        "title": fields.String(required=True),
        "description": fields.String(),
        "price": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "amenities": fields.List(fields.String, required=False),
    },
)


place_update_model = api.model(
    "PlaceUpdate",
    {
        "title": fields.String(),
        "description": fields.String(),
        "price": fields.Float(),
        "latitude": fields.Float(),
        "longitude": fields.Float(),
        "amenities": fields.List(fields.String),
    },
)


def place_to_dict(place):
    """Convert a Place object to a dictionary."""
    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner_id": place.owner_id,
    }


@api.route("/")
class PlaceList(Resource):
    """Handle operations on the places collection."""

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Missing or invalid token")
    @jwt_required()
    def post(self):
        """Create a place for the authenticated user."""
        current_user_id = get_jwt_identity()
        place_data = (request.get_json() or {}).copy()

        place_data["owner_id"] = current_user_id

        try:
            new_place = facade.create_place(place_data)
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        return place_to_dict(new_place), 201

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Return all places publicly."""
        places = facade.get_all_places()

        return [
            place_to_dict(place)
            for place in places
        ], 200


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    """Handle operations on a specific place."""

    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Return place details publicly."""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
            } if owner else None,
            "amenities": [
                {
                    "id": amenity.id,
                    "name": amenity.name,
                }
                for amenity in place.amenities
            ],
            "reviews": [
                {
                    "id": review.id,
                    "text": review.text,
                    "rating": review.rating,
                    "user_id": review.user_id,
                }
                for review in place.reviews
            ],
        }, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(401, "Missing or invalid token")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @jwt_required()
    def put(self, place_id):
        """Update a place with administrator override."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if (
            not is_admin
            and str(place.owner_id) != str(current_user_id)
        ):
            return {"error": "Unauthorized action"}, 403

        place_data = (request.get_json() or {}).copy()
        place_data.pop("owner_id", None)

        try:
            updated_place = facade.update_place(
                place_id,
                place_data
            )
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        if not updated_place:
            updated_place = facade.get_place(place_id)

        return place_to_dict(updated_place), 200

    @api.response(200, "Place deleted successfully")
    @api.response(401, "Missing or invalid token")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @jwt_required()
    def delete(self, place_id):
        """Delete a place with administrator override."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if (
            not is_admin
            and str(place.owner_id) != str(current_user_id)
        ):
            return {"error": "Unauthorized action"}, 403

        try:
            facade.delete_place(place_id)
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        return {"message": "Place deleted successfully"}, 200


@api.route("/<string:place_id>/reviews")
class PlaceReviewList(Resource):
    """Handle reviews belonging to a place."""

    @api.response(200, "List of reviews retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Return all reviews for a place."""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_for_place(place_id)

        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id,
            }
            for review in reviews
        ], 200
