#!/usr/bin/python3
"""Review API endpoints with authentication and admin access control."""

from flask import request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace("reviews", description="Review operations")


review_model = api.model(
    "Review",
    {
        "text": fields.String(
            required=True,
            description="Text of the review"
        ),
        "rating": fields.Integer(
            required=True,
            description="Rating of the place from 1 to 5"
        ),
        "place_id": fields.String(
            required=True,
            description="ID of the place"
        ),
    },
)


review_update_model = api.model(
    "ReviewUpdate",
    {
        "text": fields.String(
            required=False,
            description="Updated review text"
        ),
        "rating": fields.Integer(
            required=False,
            description="Updated rating"
        ),
    },
)


def review_to_dict(review):
    """Convert a Review object to a dictionary."""
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user_id,
        "place_id": review.place_id,
    }


@api.route("/")
class ReviewList(Resource):
    """Handle operations on the reviews collection."""

    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Missing or invalid token")
    @jwt_required()
    def post(self):
        """Create a review for the authenticated user."""
        current_user_id = get_jwt_identity()
        review_data = (request.get_json() or {}).copy()

        place = facade.get_place(review_data.get("place_id"))

        if not place:
            return {"error": "Place not found"}, 404

        if str(place.owner_id) == str(current_user_id):
            return {
                "error": "You cannot review your own place"
            }, 400

        existing_reviews = facade.get_reviews_for_place(place.id)

        for review in existing_reviews:
            if str(review.user_id) == str(current_user_id):
                return {
                    "error": "You have already reviewed this place"
                }, 400

        review_data["user_id"] = current_user_id

        try:
            new_review = facade.create_review(review_data)
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        return review_to_dict(new_review), 201

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Return all reviews publicly."""
        reviews = facade.get_all_reviews()

        return [
            review_to_dict(review)
            for review in reviews
        ], 200


@api.route("/<string:review_id>")
class ReviewResource(Resource):
    """Handle operations on a specific review."""

    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Return a review by ID."""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        return review_to_dict(review), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(401, "Missing or invalid token")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def put(self, review_id):
        """Update a review with administrator override."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if (
            not is_admin
            and str(review.user_id) != str(current_user_id)
        ):
            return {"error": "Unauthorized action"}, 403

        review_data = (request.get_json() or {}).copy()
        review_data.pop("user_id", None)
        review_data.pop("place_id", None)

        try:
            updated_review = facade.update_review(
                review_id,
                review_data
            )
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        if not updated_review:
            updated_review = facade.get_review(review_id)

        return review_to_dict(updated_review), 200

    @api.response(200, "Review deleted successfully")
    @api.response(401, "Missing or invalid token")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def delete(self, review_id):
        """Delete a review with administrator override."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if (
            not is_admin
            and str(review.user_id) != str(current_user_id)
        ):
            return {"error": "Unauthorized action"}, 403

        try:
            facade.delete_review(review_id)
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        return {"message": "Review deleted successfully"}, 200
