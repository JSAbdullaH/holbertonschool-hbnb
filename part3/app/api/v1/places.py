#!/usr/bin/python3
"""Place API endpoints."""

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services.facade import facade


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


@api.route("/")
class PlaceList(Resource):
    """Handle place collection operations."""

    @api.expect(place_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a place for the authenticated user."""
        current_user_id = get_jwt_identity()
        data = (request.get_json() or {}).copy()

        data["owner_id"] = current_user_id

        try:
            place = facade.create_place(data)
        except ValueError as error:
            return {"error": str(error)}, 400

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
        }, 201

    def get(self):
        """Return all places without requiring authentication."""
        places = facade.get_all_places()

        return [
            {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner_id,
            }
            for place in places
        ], 200


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    """Handle operations for one place."""

    def get(self, place_id):
        """Return one place without requiring authentication."""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)

        amenities = []

        for item in place.amenities:
            if isinstance(item, str):
                amenity = facade.get_amenity(item)

                if amenity:
                    amenities.append(amenity)
            else:
                amenities.append(item)

        reviews = facade.get_reviews_for_place(place.id)

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
                for amenity in amenities
            ],
            "reviews": [
                {
                    "id": review.id,
                    "text": review.text,
                    "rating": review.rating,
                    "user_id": review.user_id,
                }
                for review in reviews
            ],
        }, 200

    @api.expect(place_update_model, validate=True)
    @jwt_required()
    def put(self, place_id):
        """Update a place owned by the authenticated user."""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if str(place.owner_id) != str(current_user_id):
            return {"error": "Unauthorized action"}, 403

        data = (request.get_json() or {}).copy()

        data.pop("owner_id", None)

        try:
            facade.update_place(place_id, data)
        except ValueError as error:
            return {"error": str(error)}, 400

        return {"message": "Place updated successfully"}, 200


@api.route("/<string:place_id>/reviews")
class PlaceReviewList(Resource):
    """Return reviews belonging to a place."""

    def get(self, place_id):
        """Return reviews for one place."""
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
            }
            for review in reviews
        ], 200
