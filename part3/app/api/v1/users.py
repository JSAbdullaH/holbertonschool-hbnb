#!/usr/bin/python3
"""User API endpoints with authentication and admin access control."""

from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace("users", description="User operations")


user_model = api.model(
    "User",
    {
        "first_name": fields.String(
            required=True,
            description="First name of the user"
        ),
        "last_name": fields.String(
            required=True,
            description="Last name of the user"
        ),
        "email": fields.String(
            required=True,
            description="Email of the user"
        ),
        "password": fields.String(
            required=True,
            description="Password of the user"
        ),
        "is_admin": fields.Boolean(
            required=False,
            description="Administrator status"
        ),
    },
)


user_update_model = api.model(
    "UserUpdate",
    {
        "first_name": fields.String(
            required=False,
            description="First name of the user"
        ),
        "last_name": fields.String(
            required=False,
            description="Last name of the user"
        ),
        "email": fields.String(
            required=False,
            description="Email of the user"
        ),
        "password": fields.String(
            required=False,
            description="Password of the user"
        ),
        "is_admin": fields.Boolean(
            required=False,
            description="Administrator status"
        ),
    },
)


def user_to_dict(user):
    """Convert a User object to a dictionary."""
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_admin": user.is_admin,
    }


@api.route("/")
class UserList(Resource):
    """Handle operations on the users collection."""

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Missing or invalid token")
    @api.response(403, "Administrator privileges required")
    @jwt_required()
    def post(self):
        """Allow an administrator to create a new user."""
        claims = get_jwt()

        if not claims.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        user_data = (api.payload or {}).copy()

        existing_user = facade.get_user_by_email(user_data["email"])

        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        return user_to_dict(new_user), 201

    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """Return all users."""
        users = facade.get_all_users()

        return [user_to_dict(user) for user in users], 200


@api.route("/<string:user_id>")
class UserResource(Resource):
    """Handle operations on a specific user."""

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Return a user by ID."""
        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return user_to_dict(user), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, "User updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(401, "Missing or invalid token")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    @jwt_required()
    def put(self, user_id):
        """Update a user with administrator support."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        user_data = (api.payload or {}).copy()

        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        if not is_admin and str(current_user_id) != str(user_id):
            return {"error": "Unauthorized action"}, 403

        if not is_admin:
            if "email" in user_data or "password" in user_data:
                return {
                    "error": "You cannot modify email or password"
                }, 400

            user_data.pop("is_admin", None)

        if "email" in user_data:
            existing_user = facade.get_user_by_email(user_data["email"])

            if (
                existing_user
                and str(existing_user.id) != str(user_id)
            ):
                return {"error": "Email already registered"}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
        except (ValueError, TypeError, KeyError) as error:
            return {"error": str(error)}, 400

        if not updated_user:
            updated_user = facade.get_user(user_id)

        return user_to_dict(updated_user), 200
