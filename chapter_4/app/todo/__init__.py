from flask import Blueprint
from flask_restful import Api
from .resources import TodoResource

todo = Blueprint('todo', __name__)
todo_api = Api(todo, catch_all_404s=True)

todo_api.add_resource(TodoResource, '/todos/', endpoint='todos')
todo_api.add_resource(TodoResource, '/todos/<todo_id>/', endpoint='todos_detail')



