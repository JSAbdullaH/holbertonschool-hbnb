#!/usr/bin/python3
"""Review API endpoints."""

from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace(
    "reviews",
    description="Review operations"
)


review_model = api.model(
    "Review",
    {
        "text": fields.String(
            required=True,
            description="Review text"
        ),
        "rating": fields.Integer(
            required=True,
            description="Rating from 1 to 5"
        ),
        "user_id": fields.String(
            required=True,
            description="User identifier"
        ),
        "place_id": fields.String(
            required=True,
            description="Place identifier"
        )
    }
)


def serialize_review(review):
    """Convert a review object to a dictionary."""
    return {
        "id": review.id,
        "text": getattr(
            review,
            "text",
            getattr(review, "comment", None)
        ),
        "rating": review.rating,
        "user_id": review.user_id,
        "place_id": review.place_id
    }


def validate_review_data(data, partial=False):
    """Validate review creation or update data."""
    required_fields = [
        "text",
        "rating",
        "user_id",
        "place_id"
    ]

    if not partial:
        for field in required_fields:
            if field not in data:
                return "{} is required".format(field)

    if "text" in data:
        if not isinstance(data["text"], str):
            return "Text must be a string"

        if not data["text"].strip():
            return "Text is required"

    if "rating" in data:
        if type(data["rating"]) is not int:
            return "Rating must be an integer"

        if data["rating"] < 1 or data["rating"] > 5:
            return "Rating must be between 1 and 5"

    return None


@api.route("/")
class ReviewList(Resource):
    """Handle the collection of reviews."""

    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "User or place not found")
    def post(self):
        """Create a new review."""
        data = request.get_json()

        if not isinstance(data, dict):
            return {"error": "Invalid JSON data"}, 400

        error = validate_review_data(data)

        if error:
            return {"error": error}, 400

        user = facade.get_user(data["user_id"])

        if user is None:
            return {"error": "User not found"}, 404

        place = facade.get_place(data["place_id"])

        if place is None:
            return {"error": "Place not found"}, 404

        review_data = {
            "text": data["text"],
            "rating": data["rating"],
            "user_id": data["user_id"],
            "place_id": data["place_id"]
        }

        try:
            review = facade.create_review(review_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return serialize_review(review), 201

    @api.response(200, "Reviews successfully retrieved")
    def get(self):
        """Return all reviews."""
        reviews = facade.get_all_reviews()

        return [
            serialize_review(review)
            for review in reviews
        ], 200


@api.route("/<string:review_id>")
@api.param("review_id", "The review identifier")
class ReviewResource(Resource):
    """Handle one review."""

    @api.response(200, "Review successfully retrieved")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Return a review by ID."""
        review = facade.get_review(review_id)

        if review is None:
            return {"error": "Review not found"}, 404

        return serialize_review(review), 200

    @api.expect(review_model)
    @api.response(200, "Review successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "Review not found")
    def put(self, review_id):
        """Update an existing review."""
        review = facade.get_review(review_id)

        if review is None:
            return {"error": "Review not found"}, 404

        data = request.get_json()

        if not isinstance(data, dict):
            return {"error": "Invalid JSON data"}, 400

        error = validate_review_data(data, partial=True)

        if error:
            return {"error": error}, 400

        if "user_id" in data:
            user = facade.get_user(data["user_id"])

            if user is None:
                return {"error": "User not found"}, 404

        if "place_id" in data:
            place = facade.get_place(data["place_id"])

            if place is None:
                return {"error": "Place not found"}, 404

        try:
            updated_review = facade.update_review(
                review_id,
                data
            )
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        if updated_review is None:
            return {"error": "Review not found"}, 404

        return serialize_review(updated_review), 200

    @api.response(200, "Review successfully deleted")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review."""
        review = facade.get_review(review_id)

        if review is None:
            return {"error": "Review not found"}, 404

        facade.delete_review(review_id)

        return {"message": "Review deleted successfully"}, 200


@api.route("/places/<string:place_id>/reviews")
@api.param("place_id", "The place identifier")
class PlaceReviewList(Resource):
    """Handle reviews belonging to a place."""

    @api.response(200, "Reviews successfully retrieved")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Return all reviews for a specific place."""
        place = facade.get_place(place_id)

        if place is None:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)

        return [
            serialize_review(review)
            for review in reviews
        ], 200
