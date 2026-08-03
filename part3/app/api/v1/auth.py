from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication Operation')

login_model = api.model('login', {'email': fields.String(requierd=True, descreption='user email'), 'password': fields.String(requierd=True, descreption='User Password')})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id, additional_claims={'is_admin': user.is_admin})
        return {'access_token': access_token}, 200