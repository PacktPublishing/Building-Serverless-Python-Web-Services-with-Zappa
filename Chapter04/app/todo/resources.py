from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import current_identity, jwt_required

from .models import Todo


class TodoResource(Resource):

    decorators = [jwt_required()]

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', type=str, required=True)

        args = parser.parse_args(strict=True)
        todo = Todo(args['title'], created_by=current_identity.email).save()
        return todo.to_dict(), 201

    def get(self, todo_id=None):
        if todo_id:
            todos = Todo.query.filter_by(id=todo_id, created_by=current_identity.email)
        else:
            todos = Todo.query.filter_by(created_by=current_identity.email)
        return [todo.to_dict() for todo in todos]

    def patch(self, todo_id=None):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'status',
            choices=('open', 'completed'),
            help='Bad choice: {error_msg}. Valid choices are \'open\' or \'completed\'.',
            required=True)

        if not todo_id:
            return {'error': 'method not allowed'}, 405
        args = parser.parse_args(strict=True)
        todo = Todo.query.filter_by(id=todo_id, created_by=current_identity.email).scalar()
        if args['status'] == "open":
            todo.reopen()
        elif args['status'] == 'completed':
            todo.completed()
        else:
            return {'error':'Invalid data!'}, 400
        return todo.to_dict(), 202

    def delete(self, todo_id=None):
        if not todo_id:
            return {'error': 'method not allowed'}, 405
        Todo.query.filter_by(id=int(todo_id), created_by=current_identity.email).delete()
        return {}, 204
