import unittest
from app import create_app


class TestHBnBEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def make_user(self, email):
        return self.client.post('/api/v1/users/', json={
            "first_name": "Jane", "last_name": "Doe", "email": email})

    def make_place(self, owner_id):
        return self.client.post('/api/v1/places/', json={
            "title": "Villa", "description": "Nice", "price": 200.0,
            "latitude": 24.7, "longitude": 46.6,
            "owner_id": owner_id, "amenities": []})

    # ----- Users -----
    def test_create_user(self):
        response = self.make_user("u1@example.com")
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "", "last_name": "", "email": "invalid-email"})
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        self.make_user("dup@example.com")
        response = self.make_user("dup@example.com")
        self.assertEqual(response.status_code, 400)

    def test_get_users_list(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_not_found(self):
        response = self.client.get('/api/v1/users/no-such-id')
        self.assertEqual(response.status_code, 404)

    # ----- Amenities -----
    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_get_amenity_not_found(self):
        response = self.client.get('/api/v1/amenities/no-such-id')
        self.assertEqual(response.status_code, 404)

    # ----- Places -----
    def test_create_place(self):
        owner_id = self.make_user("p1@example.com").json['id']
        response = self.make_place(owner_id)
        self.assertEqual(response.status_code, 201)

    def test_create_place_negative_price(self):
        owner_id = self.make_user("p2@example.com").json['id']
        response = self.client.post('/api/v1/places/', json={
            "title": "Villa", "description": "Nice", "price": -10,
            "latitude": 24.7, "longitude": 46.6,
            "owner_id": owner_id, "amenities": []})
        self.assertEqual(response.status_code, 400)

    def test_create_place_out_of_range_latitude(self):
        owner_id = self.make_user("p3@example.com").json['id']
        response = self.client.post('/api/v1/places/', json={
            "title": "Villa", "description": "Nice", "price": 100,
            "latitude": 100, "longitude": 46.6,
            "owner_id": owner_id, "amenities": []})
        self.assertEqual(response.status_code, 400)

    def test_get_place_not_found(self):
        response = self.client.get('/api/v1/places/no-such-id')
        self.assertEqual(response.status_code, 404)

    # ----- Reviews -----
    def test_create_review(self):
        owner_id = self.make_user("r1@example.com").json['id']
        place_id = self.make_place(owner_id).json['id']
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great!", "rating": 5,
            "user_id": owner_id, "place_id": place_id})
        self.assertEqual(response.status_code, 201)

    def test_create_review_empty_text(self):
        owner_id = self.make_user("r2@example.com").json['id']
        place_id = self.make_place(owner_id).json['id']
        response = self.client.post('/api/v1/reviews/', json={
            "text": "", "rating": 5,
            "user_id": owner_id, "place_id": place_id})
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        owner_id = self.make_user("r3@example.com").json['id']
        place_id = self.make_place(owner_id).json['id']
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great!", "rating": 5,
            "user_id": "no-such-user", "place_id": place_id})
        self.assertEqual(response.status_code, 400)

    def test_delete_review(self):
        owner_id = self.make_user("r4@example.com").json['id']
        place_id = self.make_place(owner_id).json['id']
        review_id = self.client.post('/api/v1/reviews/', json={
            "text": "Great!", "rating": 5,
            "user_id": owner_id, "place_id": place_id}).json['id']
        response = self.client.delete('/api/v1/reviews/' + review_id)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/reviews/' + review_id)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
