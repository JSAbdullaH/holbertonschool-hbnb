#!/usr/bin/python3
"""Users API endpoints."""

from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace(
    "users",
    description="Operations related to users"
)

user_model = api.model(
    "User",
    {
        "username": fields.String(
            required=True,
            description="User username"
        ),
        "email": fields.String(
            required=True,
            description="User email"
        ),
        "password": fields.String(
            required=True,
            description="User password"
        )
    }
)

user_response = api.model(
    "UserResponse",
    {
        "id": fields.String,
        "username": fields.String,
        "email": fields.String
    }
)


def serialize_user(user):
    """Convert User object to dictionary."""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }


def validate_user_data(data, partial=False):
    """Validate user data."""

    if not data:
        return False, "No input data provided"

    required_fields = ["username", "email", "password"]

    if not partial:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

    if "email" in data and "@" not in data["email"]:
        return False, "Invalid email format"

    if "password" in data and len(data["password"]) < 6:
        return False, "Password must be at least 6 characters long"

    return True, None


@api.route("/")
class UserList(Resource):
    """User collection endpoints."""

    @api.marshal_list_with(user_response)
    def get(self):
        """Return all users."""
        users = facade.get_all_users()
        return [serialize_user(user) for user in users], 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response, code=201)
    def post(self):
        """Create a new user."""

        data = request.get_json()

        valid, error = validate_user_data(data)

        if not valid:
            return {"error": error}, 400

        user = facade.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )

        return serialize_user(user), 201


@api.route("/<string:user_id>")
@api.param("user_id", "User ID")
class User(Resource):
    """Single user endpoints."""

    @api.marshal_with(user_response)
    def get(self, user_id):
        """Return one user."""

        user = facade.get_user(user_id)

        if user is None:
            return {"error": "User not found"}, 404

        return serialize_user(user), 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response)
    def put(self, user_id):
        """Update a user."""

        user = facade.get_user(user_id)

        if user is None:
            return {"error": "User not found"}, 404

        data = request.get_json()

        valid, error = validate_user_data(data, partial=True)

        if not valid:
            return {"error": error}, 400

        updated_user = facade.update_user(user_id, data)

        return serialize_user(updated_user), 200