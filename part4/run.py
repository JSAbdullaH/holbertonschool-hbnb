from flask import Flask, render_template
from flask_restx import Api
from flask_jwt_extended import JWTManager

from app.api.v1.places import api as places_api
from app.api.v1.auth import api as auth_api
from app.api.v1.reviews import api as reviews_api
from app.api.v1.users import api as users_api
from app.api.v1.amenities import api as amenities_api

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', prefix='/api/v1', doc='/api/v1/docs')

api.add_namespace(places_api)
api.add_namespace(auth_api)
api.add_namespace(reviews_api)
api.add_namespace(users_api)
api.add_namespace(amenities_api)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/place')
def place():
    return render_template('place.html')

@app.route('/add_review')
def add_review():
    return render_template('add_review.html')

from app.services import facade

def seed_data():
    
    admin = facade.create_user({
        'first_name': 'Admin', 'last_name': 'System',
        'email': 'admin@hbnb.com', 'password': 'password123', 'is_admin': True
    })
    
    owner = facade.create_user({
        'first_name': 'John', 'last_name': 'Owner',
        'email': 'owner@hbnb.com', 'password': 'password123', 'is_admin': False
    })
    
    user = facade.create_user({
        'first_name': 'Ahmad', 'last_name': 'User',
        'email': 'user@hbnb.com', 'password': 'password123', 'is_admin': False
    })

    wifi = facade.create_amenity({'name': 'WiFi'})
    pool = facade.create_amenity({'name': 'Swimming Pool'})
    ac = facade.create_amenity({'name': 'Air Conditioning'})

    place1 = facade.create_place({
        'title': 'VillaRiyadh',
        'description': 'A beautiful villa with a private pool in Riyadh.',
        'price': 250.0,
        'latitude': 24.7136,
        'longitude': 46.6753,
        'owner_id': owner.id,
        'amenities': [wifi.id, pool.id, ac.id]
    })
    
    place2 = facade.create_place({
        'title': 'JeddahBeachApartment',
        'description': 'Nice apartment near the sea with great views.',
        'price': 85.0,
        'latitude': 21.4858,
        'longitude': 39.1925,
        'owner_id': owner.id,
        'amenities': [wifi.id, ac.id]
    })

    facade.create_review({
        'text': 'المكان رائع جداً وأنصح به بقوة!',
        'rating': 5,
        'user_id': user.id,
        'place_id': place1.id
    })
    
    facade.create_review({
        'text': 'جيد ولكن يحتاج إلى بعض النظافة الإضافية.',
        'rating': 3,
        'user_id': user.id,
        'place_id': place2.id
    })
    

try:
    if not facade.get_all_users():
        seed_data()
except Exception as e:
    print(f"No DATA :  {e}")

if __name__ == '__main__':
    app.run(debug=True)