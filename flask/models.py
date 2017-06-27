"""."""
from app import db


class Task(db.Model):
    """."""

    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(length=256, convert_unicode=True), nullable=False
    )
    category = db.Column(db.String(length=32, convert_unicode=True))
    due_date = db.Column(db.DateTime())
    complete = db.Column(db.Boolean())

    def __init__(self, title, category=None, due_date=None, complete=False):
        """."""
        self.title = title
        self.category = category
        self.due_date = due_date
        self.complete = complete

    def __repr__(self):
        """."""
        fill_string = '<Task {}: {} | completed: {}>'
        return fill_string.format(self.id, self.title[:50], self.complete)
