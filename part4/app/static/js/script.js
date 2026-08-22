const API_BASE_URL = 'http://127.0.0.1:5000'; // تأكد أن هذا هو رابط السيرفر الخاص بك

// 1. تسجيل الدخول
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token); // حفظ الـ Token
                window.location.href = '/'; // التوجيه للرئيسية
            } else {
                alert('بيانات الدخول غير صحيحة');
            }
        } catch (error) {
            console.error('Login error:', error);
        }
    });
}

// 2. جلب الأماكن في الصفحة الرئيسية
const placesList = document.getElementById('places-list-container');
if (placesList) {
    async function loadPlaces() {
        try {
            const response = await fetch(`${API_BASE_URL}/places/`);
            const places = await response.json();
            
            placesList.innerHTML = ''; 
            places.forEach(place => {
                const card = document.createElement('article');
                card.className = 'place-card';
                // الواجهة الخلفية تُرجع id, title, latitude, longitude فقط في القائمة
                card.innerHTML = `
                    <h2>${place.title}</h2>
                    <p>Location: ${place.latitude}, ${place.longitude}</p>
                    <a href="/place.html?id=${place.id}" class="details-button">View Details</a>
                `;
                placesList.appendChild(card);
            });
        } catch (error) {
            console.error('Error loading places:', error);
        }
    }
    loadPlaces();
}

// 3. جلب تفاصيل مكان محدد
const placeDetailsContainer = document.getElementById('place-details-container');
if (placeDetailsContainer) {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (placeId) {
        async function loadPlaceDetails() {
            try {
                const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
                const place = await response.json();
                
                document.getElementById('place-title').innerText = place.title;
                document.getElementById('place-price').innerText = `$${place.price} / night`;
                document.getElementById('place-desc').innerText = place.description;
                document.getElementById('place-host').innerText = `${place.owner.first_name} ${place.owner.last_name}`;
            } catch (error) {
                console.error('Error loading details:', error);
            }
        }
        loadPlaceDetails();
    }
}