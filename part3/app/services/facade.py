#!/usr/bin/python3
"""Facade layer for HBnB business operations."""

from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app.persistence.user_repository import UserRepository


class HBnBFacade:
    """Provide a unified interface to application repositories."""

    def __init__(self):
        """Initialize repositories."""
        self.user_repo = UserRepository()

        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # -------------------- Users --------------------

    def create_user(self, user_data):
        """Create and store a new user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Return a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Return a user by email."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Return all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """Update a user and return the updated object."""
        return self.user_repo.update(user_id, data)

    def delete_user(self, user_id):
        """Delete a user."""
        return self.user_repo.delete(user_id)

    # -------------------- Places --------------------

    def create_place(self, place_data):
        """Create and store a new place."""
        data = dict(place_data)

        owner_id = data.pop("owner_id", None)
        owner = self.user_repo.get(owner_id)

        if not owner:
            raise ValueError("Invalid owner_id")

        amenity_ids = data.pop("amenities", [])

        place = Place(owner=owner, **data)

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)

            if not amenity:
                raise ValueError(
                    "Invalid amenity ID: {}".format(amenity_id)
                )

            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Return a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Return all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place."""
        data = dict(place_data)

        data.pop("owner_id", None)

        amenity_ids = data.pop("amenities", None)

        place = self.place_repo.update(place_id, data)

        if not place:
            return None

        if amenity_ids is not None:
            place.amenities = []

            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)

                if not amenity:
                    raise ValueError(
                        "Invalid amenity ID: {}".format(amenity_id)
                    )

                place.add_amenity(amenity)

        return place

    def delete_place(self, place_id):
        """Delete a place."""
        place = self.place_repo.get(place_id)

        if not place:
            return None

        reviews = list(getattr(place, "reviews", []))

        for review in reviews:
            self.review_repo.delete(review.id)

        return self.place_repo.delete(place_id)

    # -------------------- Reviews --------------------

    def create_review(self, review_data):
        """Create and store a new review."""
        data = dict(review_data)

        user_id = data.pop("user_id", None)
        place_id = data.pop("place_id", None)

        user = self.user_repo.get(user_id)

        if not user:
            raise ValueError("Invalid user_id")

        place = self.place_repo.get(place_id)

        if not place:
            raise ValueError("Invalid place_id")

        review = Review(
            place=place,
            user=user,
            **data
        )

        place.add_review(review)
        self.review_repo.add(review)

        return review

    def get_review(self, review_id):
        """Return a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Return all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Return all reviews belonging to a place."""
        place = self.place_repo.get(place_id)

        if not place:
            return None

        return place.reviews

    def get_reviews_for_place(self, place_id):
        """Return all reviews belonging to a place."""
        reviews = self.get_reviews_by_place(place_id)

        if reviews is None:
            return []

        return reviews

    def update_review(self, review_id, review_data):
        """Update a review."""
        data = dict(review_data)

        data.pop("user_id", None)
        data.pop("place_id", None)

        if "rating" in data:
            rating = data["rating"]

            if (
                not isinstance(rating, int)
                or not 1 <= rating <= 5
            ):
                raise ValueError(
                    "rating must be an integer between 1 and 5"
                )

        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        """Delete a review."""
        review = self.review_repo.get(review_id)

        if not review:
            return None

        if (
            hasattr(review, "place")
            and review.place
            and review in review.place.reviews
        ):
            review.place.reviews.remove(review)

        return self.review_repo.delete(review_id)

    # -------------------- Amenities --------------------

    def create_amenity(self, amenity_data):
        """Create and store a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Return an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Return all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """Update an amenity."""
        return self.amenity_repo.update(amenity_id, data)

    def delete_amenity(self, amenity_id):
        """Delete an amenity."""
        return self.amenity_repo.delete(amenity_id)


facade = HBnBFacade()
