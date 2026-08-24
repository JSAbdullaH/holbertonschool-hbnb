const API_URL = 'http://127.0.0.1:5000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthentication(); 
        setupFilter();
    }

    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        checkPlaceAuthentication(); 
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) loginForm.addEventListener('submit', handleLogin);

    const reviewForm = document.getElementById('review-form') || document.getElementById('add-review-form');
    if (reviewForm) {
        const token = checkAuthenticationForReview();
        const placeId = getPlaceIdFromURL();

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const reviewText = document.getElementById('review-text') ? document.getElementById('review-text').value : document.getElementById('comment').value;
            const rating = document.getElementById('rating') ? document.getElementById('rating').value : 5;
            
            await submitReview(token, placeId, reviewText, rating);
        });
    }
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

function checkPlaceAuthentication() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review-section');
    const placeId = getPlaceIdFromURL();

    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
            
            addReviewSection.innerHTML = `
                <a href="/add_review?place_id=${placeId}" class="add-review details-button" style="display: inline-block;">Add Review</a>
            `;
        }
    }

    if (placeId) {
        fetchPlaceDetails(token, placeId);
    }
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
        
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details');
            document.getElementById('place-details').innerHTML = '<p>Place not found.</p>';
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}


function displayPlaceDetails(place) {
    const titleEl = document.getElementById('place-title');
    const hostEl = document.getElementById('place-host');
    const priceEl = document.getElementById('place-price');
    const descEl = document.getElementById('place-desc');
    const amenitiesEl = document.getElementById('place-amenities');

    if (titleEl) titleEl.textContent = place.title;
    
    if (hostEl) {
        hostEl.textContent = place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Unknown';
    }
    
    if (priceEl) priceEl.textContent = `$${place.price} / night`;
    if (descEl) descEl.textContent = place.description;
    
    if (amenitiesEl) {
        amenitiesEl.textContent = (place.amenities && place.amenities.length > 0) 
            ? place.amenities.map(a => a.name).join(', ') 
            : 'No amenities listed';
    }

    const reviewsContainer = document.getElementById('reviews-container');
    if (reviewsContainer) {
        reviewsContainer.innerHTML = ''; 
        
        if (place.reviews && place.reviews.length > 0) {
            place.reviews.forEach(review => {
                reviewsContainer.innerHTML += `
                    <article class="review-card">
                        <p><strong>Rating:</strong> ${review.rating}/5</p>
                        <p>${review.text}</p>
                    </article>
                `;
            });
        } else {
            reviewsContainer.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
        }
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    const authNav = document.getElementById('auth-nav');
    const loginLink = document.getElementById('login-link');
    
    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (authNav && !document.getElementById('logout-button')) {
            const logoutBtn = document.createElement('button');
            logoutBtn.id = 'logout-button';
            logoutBtn.className = 'login-button';
            logoutBtn.textContent = 'Logout';
            logoutBtn.addEventListener('click', () => {
                document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                window.location.reload(); 
            });
            authNav.appendChild(logoutBtn);
        }
    } else {
        if (loginLink) loginLink.style.display = 'block';
    }
    fetchPlaces(token);
}

async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_URL}/places/`, { headers });
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    if (!container) return;
    container.innerHTML = '';

    places.forEach(place => {
        const article = document.createElement('article');
        article.className = 'premium-place-card'; 
        const price = place.price || 0; 
        article.setAttribute('data-price', price);
        
        let imageUrl = `https://picsum.photos/seed/${place.id}/600/400`;

        if (place.title === 'VillaRiyadh') {
            imageUrl = 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80';
        } 
        else if (place.title === 'JeddahBeachApartment') {
            imageUrl = 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80';
        }
       
        article.innerHTML = `
            <div class="card-image-wrapper">
                <img src="${imageUrl}" alt="${place.title}" class="place-cover">
                <div class="guest-favorite-badge">Guest favorite</div>
                <button class="favorite-btn"><i class="fa-regular fa-heart"></i></button>
            </div>
            <div class="card-content">
                <div class="card-header">
                    <h3>${place.title}</h3>
                    <span class="rating"><i class="fa-solid fa-star"></i> 4.9</span>
                </div>
                <p class="location"><i class="fa-solid fa-location-dot"></i> ${place.latitude}, ${place.longitude}</p>
                <p class="price"><strong>$${price}</strong> / night</p>
                <a href="/place?id=${place.id}" class="card-btn">View Details</a>
            </div>
        `;
        container.appendChild(article);
    });
}

function setupFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const placeCards = document.querySelectorAll('#places-list .place-card');
            
            placeCards.forEach(card => {
                const placePrice = parseFloat(card.getAttribute('data-price'));
                if (selectedPrice === 'All' || placePrice <= parseFloat(selectedPrice)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
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
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = '/'; 
        } else {
            alert('Login failed: ' + response.statusText);
        }
    } catch (error) {
        console.error('Login error:', error);
    }
}

async function handleAddReview(e) {
    e.preventDefault();
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id');
    const token = getCookie('token');

    if (!token || !placeId) {
        alert('You must be logged in and specify a place.');
        return;
    }

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
            window.location.href = `/place?id=${placeId}`;
        } else {
            alert('Failed to add review.');
        }
    } catch (error) {
        console.error('Error adding review:', error);
    }
}

function checkAuthenticationForReview() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/';
    }
    return token;
}

async function submitReview(token, placeId, reviewText, rating) {
    if (!placeId) {
        alert('Place ID is missing!');
        return;
    }

    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = payload.sub;

    try {
        const response = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                user_id: userId,
                place_id: placeId
            })
        });

        handleReviewResponse(response, placeId);
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting the review.');
    }
}

function handleReviewResponse(response, placeId) {
    if (response.ok) {
        alert('Review submitted successfully!');
        const reviewForm = document.getElementById('review-form') || document.getElementById('add-review-form');
        if (reviewForm) reviewForm.reset();
        
        window.location.href = `/place?id=${placeId}`;
    } else {
        alert('Failed to submit review');
    }
}