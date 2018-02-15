from flask import Blueprint

todo = Blueprint('todo', __name__)

from . import views