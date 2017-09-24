# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app import db
from datetime import datetime


class Profile(db.Model):
    """The Profile model for an individual user."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, index=True, unique=True)
    email = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    tasks = db.relationship('Task', backref='profile', lazy='dynamic')

    def __init__(self, **kwargs):
        """Constructor for the Profile object."""
        super(Profile, self).__init__(**kwargs)
        self.date_joined = datetime.now()


class Task(db.Model):
    """The model for an individual To Do-list task."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    note = db.Column(db.Unicode)
    creation_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        """Constructor for the Task object."""
        super(Task, self).__init__(**kwargs)
        self.creation_date = datetime.now()
