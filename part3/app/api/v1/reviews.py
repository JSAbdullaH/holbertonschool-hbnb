#!/usr/bin/python3
"""Review API endpoints."""

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services.facade import facade


api = Namespace("reviews", description="Review operations")


review_model = api.model(
    "Review",
    {
        "text": fields.String(
            required=True,
            description="Text of the review",
        ),
        "rating": fields.Integer(
            required=True,
            description="Rating from 1 to 5",
        ),
        "place_id": fields.String(
            required=True,
            description="Place ID",
        ),
    },
)


review_update_model = api.model(
    "ReviewUpdate",
    {
        "text": fields.String(description="Updated review text"),
        "rating": fields.Integer(description="Updated rating"),
    },
)


@api.route("/")
class ReviewList(Resource):
    """Handle review collection operations."""

    @api.expect(review_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a review for the authenticated user."""
        current_user_id = get_jwt_identity()
        data = (request.get_json() or {}).copy()

        place = facade.get_place(data.get("place_id"))

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

        data["user_id"] = current_user_id

        try:
            review = facade.create_review(data)
        except ValueError as error:
            return {"error": str(error)}, 400

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
        }, 201

    def get(self):
        """Return all reviews."""
        reviews = facade.get_all_reviews()

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


@api.route("/<string:review_id>")
class ReviewResource(Resource):
    """Handle operations for one review."""

    def get(self, review_id):
        """Return one review."""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
        }, 200

    @api.expect(review_update_model, validate=True)
    @jwt_required()
    def put(self, review_id):
        """Update a review created by the authenticated user."""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if str(review.user_id) != str(current_user_id):
            return {"error": "Unauthorized action"}, 403

        data = (request.get_json() or {}).copy()

        data.pop("user_id", None)
        data.pop("place_id", None)

        try:
            facade.update_review(review_id, data)
        except ValueError as error:
            return {"error": str(error)}, 400

        return {"message": "Review updated successfully"}, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review created by the authenticated user."""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if str(review.user_id) != str(current_user_id):
            return {"error": "Unauthorized action"}, 403

        try:
            facade.delete_review(review_id)
        except ValueError:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200#!/usr/bin/python3
"""Review API endpoints."""

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services.facade import facade


api = Namespace("reviews", description="Review operations")


review_model = api.model(
    "Review",
    {
        "text": fields.String(
            required=True,
            description="Text of the review",
        ),
        "rating": fields.Integer(
            required=True,
            description="Rating from 1 to 5",
        ),
        "place_id": fields.String(
            required=True,
            description="Place ID",
        ),
    },
)


review_update_model = api.model(
    "ReviewUpdate",
    {
        "text": fields.String(description="Updated review text"),
        "rating": fields.Integer(description="Updated rating"),
    },
)


@api.route("/")
class ReviewList(Resource):
    """Handle review collection operations."""

    @api.expect(review_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a review for the authenticated user."""
        current_user_id = get_jwt_identity()
        data = (request.get_json() or {}).copy()

        place = facade.get_place(data.get("place_id"))

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

        data["user_id"] = current_user_id

        try:
            review = facade.create_review(data)
        except ValueError as error:
            return {"error": str(error)}, 400

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
        }, 201

    def get(self):
        """Return all reviews."""
        reviews = facade.get_all_reviews()

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


@api.route("/<string:review_id>")
class ReviewResource(Resource):
    """Handle operations for one review."""

    def get(self, review_id):
        """Return one review."""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
        }, 200

    @api.expect(review_update_model, validate=True)
    @jwt_required()
    def put(self, review_id):
        """Update a review created by the authenticated user."""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if str(review.user_id) != str(current_user_id):
            return {"error": "Unauthorized action"}, 403

        data = (request.get_json() or {}).copy()

        data.pop("user_id", None)
        data.pop("place_id", None)

        try:
            facade.update_review(review_id, data)
        except ValueError as error:
            return {"error": str(error)}, 400

        return {"message": "Review updated successfully"}, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review created by the authenticated user."""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if str(review.user_id) != str(current_user_id):
            return {"error": "Unauthorized action"}, 403

        try:
            facade.delete_review(review_id)
        except ValueError:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200
