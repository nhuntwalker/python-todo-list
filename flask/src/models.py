"""."""
from app import db
from sqlalchemy_utils.types.choice import ChoiceType


CATEGORIES = [
    ('W', 'work'), ('S', 'school'), ('P', 'personal')
]


class Task(db.Model):
    """The Task model."""

    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(length=256, convert_unicode=True), nullable=False
    )
    category = db.Column(ChoiceType(CATEGORIES))
    due_date = db.Column(db.DateTime())
    complete = db.Column(db.Boolean())
    profile = db.relationship('Profile', back_populates='tasks')
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __init__(self, title, category=None, due_date=None, complete=False):
        """Construct a new Task."""
        self.title = title
        self.category = category
        self.due_date = due_date
        self.complete = complete

    def __repr__(self):
        """String representation."""
        fill_string = '<Task {}: {} | completed: {}>'
        return fill_string.format(self.id, self.title[:50], self.complete)


class Profile(db.Model):
    """The Profile model."""

    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(length=256, convert_unicode=True),
        nullable=False
    )
    email = db.Column(
        db.String(length=256, convert_unicode=True),
        nullable=False
    )
    password = db.Column(
        db.String(length=24),
        nullable=False
    )
    tasks = db.relationship('Task', back_populates='profile')

    def __init__(self, username=None, email=None, password=None):
        """Construct a new user profile."""
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        """String representation."""
        fill_string = '<{} id:{} email:{}>'
        return fill_string.format(
            self.username, self.id, self.email
        )

db.Index('usernames', Profile.username, unique=True)
db.Index('user_emails', Profile.email, unique=True)
