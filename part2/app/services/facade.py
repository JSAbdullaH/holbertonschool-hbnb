#!/usr/bin/python3
"""Facade layer."""
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ----- Users -----
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

    # ----- Places -----
    def create_place(self, place_data):
        data = dict(place_data)
        owner_id = data.pop('owner_id', None)
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Invalid owner_id")
        amenity_ids = data.pop('amenities', [])
        place = Place(owner=owner, **data)
        for a_id in amenity_ids:
            amenity = self.amenity_repo.get(a_id)
            if not amenity:
                raise ValueError("Invalid amenity ID: " + str(a_id))
            place.add_amenity(amenity)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        data = dict(place_data)
        data.pop('owner_id', None)
        data.pop('amenities', None)
        self.place_repo.update(place_id, data)
        return self.place_repo.get(place_id)

    # ----- Reviews -----
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        self.review_repo.update(review_id, data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

    # ----- Amenities -----
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        self.amenity_repo.update(amenity_id, data)
        return self.amenity_repo.get(amenity_id)


facade = HBnBFacade()
