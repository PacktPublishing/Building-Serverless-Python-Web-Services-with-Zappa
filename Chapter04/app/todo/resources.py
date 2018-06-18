from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import current_identity, jwt_required
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

from .models import Todo

class TodoResource(Resource):

    decorators = [jwt_required()]
    add_args = {
        'description': fields.Str(
            required=True,
        )
    }
    update_args = {
        'status': fields.Str(
            required = True,
            validate = validate.OneOf(['open', 'finished'])
        )
    }

    @use_kwargs(add_args)
    def post(self, description):
        todo = Todo(description, creator=current_identity.email).save()
        return todo.to_dict(), 201

    def get(self, todo_id=None):
        if todo_id:
            todos = Todo.query.filter_by(id=todo_id, creator=current_identity.email)
        else:
            todos = Todo.query.filter_by(creator=current_identity.email)
        return [todo.to_dict() for todo in todos]

    @use_kwargs(update_args)
    def put(self, status, todo_id=None):
        if not todo_id:
            return {'error': 'method not allowed'}, 405
        todo = Todo.query.filter_by(id=todo_id, creator=current_identity.email).scalar()
        if status == "open":
            todo.reopen()
        elif status == 'finished':
            todo.finished()
        else:
            return {'error':'Invalid data!'}, 400
        return todo.to_dict(), 202

    def delete(self, todo_id=None):
        if not todo_id:
            return {'error': 'method not allowed'}, 405
        Todo.query.filter_by(id=int(todo_id), creator=current_identity.email).delete()
        return {}, 202
