# HBnB Part 2 - Testing Report

## 1. Model-Level Validation
Implemented in all entity models (Task 1):
- User: first_name/last_name required (max 50 chars), email required + format check + unique
- Place: title required (max 100), price positive, latitude [-90, 90], longitude [-180, 180], owner must be a valid User
- Review: text required, rating integer 1-5, place and user must reference valid entities
- Amenity: name required (max 50 chars)

## 2. Manual Black-Box Testing (cURL)

| # | Endpoint | Input | Expected | Actual | Result |
|---|----------|-------|----------|--------|--------|
| 1 | POST /api/v1/users/ | valid user data | 201 + user with id | 201 + user with id | PASS |
| 2 | POST /api/v1/users/ | duplicate email | 400 "Email already registered" | 400 | PASS |
| 3 | GET /api/v1/users/ | - | 200 + list | 200 + list | PASS |
| 4 | PUT /api/v1/users/<id> | new names | 200 + updated user | 200 + updated user | PASS |
| 5 | PUT /api/v1/users/<bad-id> | any | 404 "User not found" | 404 | PASS |
| 6 | POST /api/v1/amenities/ | {"name": "Wi-Fi"} | 201 + amenity | 201 + amenity | PASS |
| 7 | PUT /api/v1/amenities/<id> | new name | 200 + message | 200 + message | PASS |
| 8 | POST /api/v1/places/ | valid data + owner_id | 201 + place | 201 + place | PASS |
| 9 | GET /api/v1/places/<id> | - | 200 + owner and amenities embedded | 200 + embedded | PASS |
| 10 | POST /api/v1/reviews/ | valid data | 201 + review | 201 + review | PASS |
| 11 | GET /api/v1/places/<id>/reviews | - | 200 + reviews list | 200 + list | PASS |
| 12 | DELETE /api/v1/reviews/<id> | - | 200 + message | 200 + message | PASS |
| 13 | GET /api/v1/places/<id>/reviews (after delete) | - | 200 + empty list | 200 + [] | PASS |

## 3. Swagger Documentation
Verified at http://127.0.0.1:5000/api/v1/ - all namespaces (users, amenities, places, reviews) and models are correctly documented.

## 4. Automated Unit Tests
File: tests/test_endpoints.py (unittest, 16 tests)
Covers positive and negative scenarios for all four entities:
required fields, email format, duplicate email, boundary testing
(negative price, out-of-range latitude), non-existent resources (404),
and review deletion.

Run: python3 -m unittest tests.test_endpoints -v
Result: 16/16 OK

## 5. Issues Encountered
- Legacy model/facade code did not match the official specification
  (wrong attribute names, missing validation); rebuilt to spec before testing.
- All tests pass after the fixes.
