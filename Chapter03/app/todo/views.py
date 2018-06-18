import json

from flask import render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from app.todo import todo
from app.todo.forms import TodoForm
from app.todo.models import Todo


@todo.route('/', methods=['GET', 'POST'])
@login_required
def list():
    context = dict()
    form = TodoForm()
    if form.validate_on_submit():
        Todo(form.title.data, created_by=current_user.email).save()
        return redirect(url_for('todo.list'))
    context['form'] = form
    context['todos'] = current_user.todos
    context['items_left'] = len([todo for todo in current_user.todos if not todo.is_completed])
    return render_template('todo/list.html', **context)


@todo.route('/<todo_id>', methods=['DELETE'])
@login_required
def remove(todo_id):
    Todo.query.filter_by(id=int(todo_id)).delete()
    return jsonify({'message': 'Todo removed successfully'})


@todo.route('/<todo_id>', methods=['PATCH'])
@login_required
def update(todo_id):
    data = json.loads([k for k in request.form.keys()][0])
    todo = Todo.query.filter_by(id=int(todo_id)).scalar()
    if data.get('status'):
        todo.finished()
    else:
        todo.reopen()
    return jsonify({'message': 'Todo updated successfully'})
