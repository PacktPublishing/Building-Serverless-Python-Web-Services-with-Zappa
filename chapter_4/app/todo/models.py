from datetime import datetime
from app import db
from app.config.models import BaseModel


class Todo(db.Model, BaseModel):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    is_finished = db.Column(db.Boolean, default=False)
    creator = db.Column(db.String(64), db.ForeignKey('user.email'))
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

    def __init__(self, description, creator=None, created_at=None):
        self.description = description
        self.creator = creator

    def __repr__(self):
        return '<{0} Todo: {1} by {2}>'.format(
            self.status, self.description, self.creator or 'None')

    @property
    def status(self):
        return 'finished' if self.is_finished else 'open'

    def finished(self):
        self.is_finished = True
        self.finished_at = datetime.utcnow()
        self.save()

    def reopen(self):
        self.is_finished = False
        self.finished_at = None
        self.save()

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
        }