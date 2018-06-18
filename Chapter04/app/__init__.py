from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt import JWT, jwt_required, current_identity

from app.config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(config[environment])

    db.init_app(app)
    migrate.init_app(app, db=db)

    from .auth.models import User

    def authenticate(email, password):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user is not None and user.verify_password(data['password']):
            return user

    def identity(payload):
        user_id = payload['identity']
        return User.query.filter_by(id=user_id).first()

    jwt = JWT(app, authenticate, identity)


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .todo import todo as todo_blueprint
    app.register_blueprint(todo_blueprint)

    return app
