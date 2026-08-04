#!/usr/bin/python3
"""User API endpoints."""

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services.facade import facade


api = Namespace("users", description="User operations")


user_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)


update_user_model = api.model(
    "UpdateUser",
    {
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
    },
)


@api.route("/")
class UserList(Resource):
    """Handle user collection operations."""

    @api.expect(user_model, validate=True)
    def post(self):
        """Create a user."""
        data = api.payload

        try:
            user = facade.create_user(data)
        except ValueError as error:
            return {"error": str(error)}, 400

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, 201

    def get(self):
        """Return all users."""
        users = facade.get_all_users()

        return [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
            for user in users
        ], 200


@api.route("/<string:user_id>")
class UserResource(Resource):
    """Handle operations for one user."""

    def get(self, user_id):
        """Return one user."""
        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, 200

    @api.expect(update_user_model, validate=True)
    @jwt_required()
    def put(self, user_id):
        """Allow an authenticated user to update their own details."""
        current_user_id = get_jwt_identity()
        data = (api.payload or {}).copy()

        if str(current_user_id) != str(user_id):
            return {"error": "Unauthorized action"}, 403

        if "email" in data or "password" in data:
            return {
                "error": "You cannot modify email or password"
            }, 400

        try:
            user = facade.update_user(user_id, data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, 200
