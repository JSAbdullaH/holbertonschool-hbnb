const API_URL = 'http://127.0.0.1:5000'

document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();

    const placesList = document.getElementById('places-list');
    if (placesList) {
        fetchPlaces();
    }

    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        if (placeId) {
            fetchPlaceDetails(placeId);
            setupAddReviewLink(placeId);
        }
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    const addReviewForm = document.getElementById('add-review-form');
    if (addReviewForm) {
        addReviewForm.addEventListener('submit', handleAddReview);
    }
});

function checkAuthStatus() {
    const token = localStorage.getItem('access_token');
    const authLink = document.getElementById('auth-link');
    
    if (token) {
        authLink.innerHTML = '<button id="logout-button" class="login-button">Logout</button>';
        document.getElementById('logout-button').addEventListener('click', () => {
            localStorage.removeItem('access_token');
            window.location.href = 'index.html';
        });
    }
}

async function fetchPlaces() {
    try {
        const response = await fetch(`${API_URL}/places/`);
        const places = await response.json();
        const container = document.getElementById('places-list');
        container.innerHTML = '';

        places.forEach(place => {
            const article = document.createElement('article');
            article.className = 'place-card';
            article.innerHTML = `
                <h2>${place.title}</h2>
                <p>Location: ${place.latitude}, ${place.longitude}</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            `;
            container.appendChild(article);
        });
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`${API_URL}/places/${placeId}`);
        const place = await response.json();

        document.getElementById('place-title').textContent = place.title;
        document.getElementById('place-host').textContent = `${place.owner.first_name} ${place.owner.last_name}`;
        document.getElementById('place-price').textContent = `$${place.price} / night`;
        document.getElementById('place-desc').textContent = place.description;
        
        const amenitiesList = place.amenities.map(a => a.name).join(', ');
        document.getElementById('place-amenities').textContent = amenitiesList;

        const reviewsContainer = document.getElementById('reviews-container');
        reviewsContainer.innerHTML = '';
        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                const reviewCard = document.createElement('article');
                reviewCard.className = 'review-card';
                reviewCard.innerHTML = `
                    <h4>User ID: ${review.user_id}</h4>
                    <p>Rating: ${review.rating}/5</p>
                    <p>${review.text}</p>
                `;
                reviewsContainer.appendChild(reviewCard);
            });
        } else {
            reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

function setupAddReviewLink(placeId) {
    const addReviewSection = document.getElementById('add-review-section');
    const token = localStorage.getItem('access_token');
    
    if (token) {
        addReviewSection.innerHTML = `<a href="add_review.html?place_id=${placeId}" class="add-review">Add Review</a>`;
    } else {
        addReviewSection.innerHTML = '<p><a href="login.html">Log in</a> to add a review.</p>';
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            window.location.href = 'index.html';
        } else {
            alert('Invalid credentials!');
        }
    } catch (error) {
        console.error('Login error:', error);
    }
}

async function handleAddReview(e) {
    e.preventDefault();
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id');
    const token = localStorage.getItem('access_token');

    if (!token || !placeId) {
        alert('You must be logged in and specify a place.');
        return;
    }

    // فك تشفير التوكن لاستخراج الـ user_id
    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = payload.sub;

    const rating = document.getElementById('rating').value;
    const text = document.getElementById('comment').value;

    try {
        const response = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify({
                text: text,
                rating: parseInt(rating),
                user_id: userId,
                place_id: placeId
            })
        });

        if (response.ok) {
            alert('Review added successfully!');
            window.location.href = `place.html?id=${placeId}`;
        } else {
            alert('Failed to add review.');
        }
    } catch (error) {
        console.error('Error adding review:', error);
    }
}