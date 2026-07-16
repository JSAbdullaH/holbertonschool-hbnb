#!/usr/bin/python3
"""Place API endpoints."""

from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace(
    "places",
    description="Place operations"
)


amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(
            readonly=True,
            description="Amenity identifier"
        ),
        "name": fields.String(
            readonly=True,
            description="Amenity name"
        )
    }
)


user_model = api.model(
    "PlaceOwner",
    {
        "id": fields.String(
            readonly=True,
            description="User identifier"
        ),
        "first_name": fields.String(
            readonly=True,
            description="Owner first name"
        ),
        "last_name": fields.String(
            readonly=True,
            description="Owner last name"
        ),
        "email": fields.String(
            readonly=True,
            description="Owner email"
        )
    }
)


place_model = api.model(
    "Place",
    {
        "title": fields.String(
            required=True,
            description="Title of the place"
        ),
        "description": fields.String(
            required=True,
            description="Description of the place"
        ),
        "price": fields.Float(
            required=True,
            description="Price per night"
        ),
        "latitude": fields.Float(
            required=True,
            description="Latitude of the place"
        ),
        "longitude": fields.Float(
            required=True,
            description="Longitude of the place"
        ),
        "owner_id": fields.String(
            required=True,
            description="Identifier of the owner"
        ),
        "amenities": fields.List(
            fields.String,
            required=False,
            description="List of amenity identifiers"
        )
    }
)


def serialize_owner(owner):
    """Return an owner as a dictionary."""
    return {
        "id": owner.id,
        "first_name": getattr(
            owner,
            "first_name",
            getattr(owner, "firstname", None)
        ),
        "last_name": getattr(
            owner,
            "last_name",
            getattr(owner, "lastname", None)
        ),
        "email": owner.email
    }


def serialize_amenity(amenity):
    """Return an amenity as a dictionary."""
    return {
        "id": amenity.id,
        "name": amenity.name
    }


def serialize_place(place):
    """Return a place as a dictionary."""
    owner = getattr(place, "owner", None)
    amenities = getattr(place, "amenities", [])

    return {
        "id": place.id,
        "title": getattr(
            place,
            "title",
            getattr(place, "name", None)
        ),
        "description": place.description,
        "price": getattr(
            place,
            "price",
            getattr(place, "price_range", None)
        ),
        "latitude": getattr(place, "latitude", None),
        "longitude": getattr(place, "longitude", None),
        "owner": (
            serialize_owner(owner)
            if owner is not None
            else None
        ),
        "amenities": [
            serialize_amenity(amenity)
            for amenity in amenities
        ]
    }


def validate_place_data(data, partial=False):
    """Validate input used to create or update a place."""
    required_fields = [
        "title",
        "description",
        "price",
        "latitude",
        "longitude",
        "owner_id"
    ]

    if not partial:
        for field in required_fields:
            if field not in data:
                return "{} is required".format(field)

    if "title" in data:
        if not isinstance(data["title"], str):
            return "Title must be a string"

        if not data["title"].strip():
            return "Title is required"

    if "description" in data:
        if not isinstance(data["description"], str):
            return "Description must be a string"

    if "price" in data:
        if not isinstance(data["price"], (int, float)):
            return "Price must be a number"

        if data["price"] < 0:
            return "Price must be a positive value"

    if "latitude" in data:
        if not isinstance(data["latitude"], (int, float)):
            return "Latitude must be a number"

        if data["latitude"] < -90 or data["latitude"] > 90:
            return "Latitude must be between -90 and 90"

    if "longitude" in data:
        if not isinstance(data["longitude"], (int, float)):
            return "Longitude must be a number"

        if data["longitude"] < -180 or data["longitude"] > 180:
            return "Longitude must be between -180 and 180"

    if "amenities" in data:
        if not isinstance(data["amenities"], list):
            return "Amenities must be a list"

    return None


@api.route("/")
class PlaceList(Resource):
    """Handle operations involving the collection of places."""

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Owner or amenity not found")
    def post(self):
        """Create a new place."""
        data = request.get_json()

        if not isinstance(data, dict):
            return {"error": "Invalid JSON data"}, 400

        error = validate_place_data(data)

        if error:
            return {"error": error}, 400

        owner = facade.get_user(data["owner_id"])

        if owner is None:
            return {"error": "Owner not found"}, 404

        amenity_ids = data.get("amenities", [])
        amenities = []

        for amenity_id in amenity_ids:
            amenity = facade.get_amenity(amenity_id)

            if amenity is None:
                return {
                    "error": (
                        "Amenity {} not found"
                        .format(amenity_id)
                    )
                }, 404

            amenities.append(amenity)

        place_data = {
            "title": data["title"],
            "description": data["description"],
            "price": data["price"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "owner_id": data["owner_id"],
            "amenities": amenity_ids
        }

        try:
            place = facade.create_place(place_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return serialize_place(place), 201

    @api.response(200, "Places successfully retrieved")
    def get(self):
        """Return all places."""
        places = facade.get_all_places()

        return [
            serialize_place(place)
            for place in places
        ], 200


@api.route("/<string:place_id>")
@api.param("place_id", "The place identifier")
class PlaceResource(Resource):
    """Handle operations involving one place."""

    @api.response(200, "Place successfully retrieved")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Return one place using its identifier."""
        place = facade.get_place(place_id)

        if place is None:
            return {"error": "Place not found"}, 404

        return serialize_place(place), 200

    @api.expect(place_model)
    @api.response(200, "Place successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "Place, owner or amenity not found")
    def put(self, place_id):
        """Update an existing place."""
        place = facade.get_place(place_id)

        if place is None:
            return {"error": "Place not found"}, 404

        data = request.get_json()

        if not isinstance(data, dict):
            return {"error": "Invalid JSON data"}, 400

        error = validate_place_data(data, partial=True)

        if error:
            return {"error": error}, 400

        if "owner_id" in data:
            owner = facade.get_user(data["owner_id"])

            if owner is None:
                return {"error": "Owner not found"}, 404

        if "amenities" in data:
            for amenity_id in data["amenities"]:
                amenity = facade.get_amenity(amenity_id)

                if amenity is None:
                    return {
                        "error": (
                            "Amenity {} not found"
                            .format(amenity_id)
                        )
                    }, 404

        try:
            updated_place = facade.update_place(
                place_id,
                data
            )
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        if updated_place is None:
            return {"error": "Place not found"}, 404

        return serialize_place(updated_place), 200
