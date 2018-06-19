from datetime import datetime
from app import db
from app.config.models import BaseModel


class Todo(db.Model, BaseModel):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    is_completed = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.String(64), db.ForeignKey('user.email'))
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

    def __init__(self, title, created_by=None, created_at=None):
        self.title = title
        self.created_by = created_by

    def __repr__(self):
        return '<{0} Todo: {1} by {2}>'.format(
            self.status, self.title, self.created_by or 'None')

    @property
    def status(self):
        return 'completed' if self.is_completed else 'open'

    def completed(self):
        self.is_completed = True
        self.save()

    def reopen(self):
        self.is_completed = False
        self.save()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_by': self.created_by,
            'status': self.status,
        }
