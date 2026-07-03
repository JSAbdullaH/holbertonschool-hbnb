# Sequence Diagrams for API Calls

This document contains four sequence diagrams showing how the three layers
(Presentation, Business Logic, Persistence) interact to handle API requests.

## 1. User Registration

A user signs up by sending their data to the API. The Facade validates the
data, checks that the email is not already used, then saves the new user.

```mermaid
sequenceDiagram
participant User
participant API as Presentation Layer (API)
participant Facade as HBnBFacade (Business Logic)
participant DB as Persistence Layer

User->>API: POST /users (first_name, last_name, email, password)
API->>Facade: create_user(user_data)
Facade->>Facade: validate data (email format, required fields)
Facade->>DB: check if email already exists
DB-->>Facade: email available
Facade->>DB: save new user
DB-->>Facade: user saved (id, created_at)
Facade-->>API: return new user object
API-->>User: 201 Created (user details)
```

## 2. Place Creation

A user creates a new place listing. The Facade verifies the owner exists
and validates the data (price, coordinates) before saving.

```mermaid
sequenceDiagram
participant User
participant API as Presentation Layer (API)
participant Facade as HBnBFacade (Business Logic)
participant DB as Persistence Layer

User->>API: POST /places (title, description, price, lat, lon)
API->>Facade: create_place(place_data, owner_id)
Facade->>DB: verify owner exists
DB-->>Facade: owner found
Facade->>Facade: validate data (price > 0, valid coordinates)
Facade->>DB: save new place
DB-->>Facade: place saved (id, created_at)
Facade-->>API: return new place object
API-->>User: 201 Created (place details)
```

## 3. Review Submission

A user submits a review for a place. The Facade verifies that both the
user and the place exist, then validates the rating before saving.

```mermaid
sequenceDiagram
participant User
participant API as Presentation Layer (API)
participant Facade as HBnBFacade (Business Logic)
participant DB as Persistence Layer

User->>API: POST /reviews (place_id, rating, comment)
API->>Facade: create_review(review_data, user_id)
Facade->>DB: verify user exists
DB-->>Facade: user found
Facade->>DB: verify place exists
DB-->>Facade: place found
Facade->>Facade: validate rating (1-5) and comment
Facade->>DB: save new review
DB-->>Facade: review saved (id, created_at)
Facade-->>API: return new review object
API-->>User: 201 Created (review details)
```

## 4. Fetching a List of Places

A user requests the list of available places. The Facade retrieves all
places from the database and returns them formatted to the API.

```mermaid
sequenceDiagram
participant User
participant API as Presentation Layer (API)
participant Facade as HBnBFacade (Business Logic)
participant DB as Persistence Layer

User->>API: GET /places
API->>Facade: get_all_places()
Facade->>DB: fetch all places
DB-->>Facade: list of places
Facade->>Facade: format place data
Facade-->>API: return places list
API-->>User: 200 OK (list of places)
```

## Summary

In all four flows, the request always follows the same path:
API → Facade → Database, and the response returns through the same path
in reverse. No layer is ever skipped, which reflects the layered
architecture and the facade pattern described in the package diagram.
