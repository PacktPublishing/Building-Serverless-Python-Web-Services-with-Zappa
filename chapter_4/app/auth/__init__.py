from flask import Blueprint
from flask_restful import Api
from .resources import SignUpResource, LoginResource

auth = Blueprint('auth', __name__)
auth_api = Api(auth, catch_all_404s=True)

auth_api.add_resource(SignUpResource, '/signup', endpoint='signup')
auth_api.add_resource(LoginResource, '/login', endpoint='login')



