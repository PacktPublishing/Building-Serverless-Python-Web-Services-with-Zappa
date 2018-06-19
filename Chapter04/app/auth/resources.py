from flask import request, jsonify
from flask_restful import Resource, reqparse, abort
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
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        args = self.parser.parse_args()
        if not User.query.filter_by(email=args['email']).scalar():
            User(
                email = args['email'],
                password = args['password']
            ).save()
            return {'message': 'Sign up successfully'}
        abort(400, message='Email already exists.')


class LoginResource(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        args = self.parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if user is not None and user.verify_password(args['password']):
            token = generate_token(user)
            return jsonify({'token': token.decode("utf-8")})
        abort(400, message='Invalid credentials')
