from flask import request, jsonify
from flask_restful import Resource
from flask_jwt import current_app
from app.auth.models import User

def generate_token(user):
    """ Currently this is workaround
    since the latest version that already has this function
    is not published on PyPI yet and we don't want
    to install the package directly from GitHub.
    See: https://github.com/mattupstate/flask-jwt/blob/9f4f3bc8dce9da5dd8a567dfada0854e0cf656ae/flask_jwt/__init__.py#L145
    """
    jwt = current_app.extensions['jwt']
    token = jwt.jwt_encode_callback(user)
    return token


class SignUpResource(Resource):
    def post(self):
        data = request.json
        if not User.query.filter_by(email=data['email']).scalar():
            User(
                email = data['email'],
                password = data['password']
            ).save()
            return {'status': 200}
        else:
            return {'status': 500, 'message': 'User already exists.'}
        return {'status': 200}


class LoginResource(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user is not None and user.verify_password(data['password']):
            token = generate_token(user)
            return jsonify({'token': str(token)})
