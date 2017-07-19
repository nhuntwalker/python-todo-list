"""."""
from flask import Flask, jsonify, url_for, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import os
from passlib.hash import pbkdf2_sha256
import re
from sqlalchemy_utils.types.choice import ChoiceType


app = Flask(__name__)
app.config.from_object(
    os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# from models import Task, Profile

# MODELS

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

# VIEWS


@app.route('/api/v1/home')
def home_view():
    """The home page for the to do list app."""
    context = {
        'title': 'Python To Do | Home',
        'login': url_for('login'),
        'register': url_for('register'),
        'profile': url_for('profile', user_name='foo')
    }
    return jsonify(context), 200


@app.route('/api/v1/login', methods=['GET', 'POST'])
def login():
    """Log a user in and authenticate."""
    errors = []
    context = {}
    if request.method == "POST":
        username = request.json.get('username')
        password = request.json.get('password')
        if not username or not password:
            msg = "You are missing a username and/or password."
            errors.append(msg)
            context['username'] = username
            return jsonify(context), 200

        profile = db.session.query(Profile).filter(
            Profile.username == username
        ).all()

        if not profile or not pbkdf2_sha256.verify(password, Profile.password):
            msg = "The username or password provided is incorrect. "
            msg += "Please try again."
            errors.append(msg)

        if not errors:
            

    context["errors"] = errors
    return jsonify(context), 200


@app.route('/api/v1/logout')
@auth.login_required
def logout():
    """."""
    return ""


@app.route('/api/v1/register', methods=['GET', 'POST'])
def register():
    """Create a new user with email and password."""
    errors = []
    if request.method == "POST":
        username = request.json.get('username')
        email = request.json.get('email')
        pwd1 = request.json.get('password')
        pwd2 = request.json.get('password2')
        if len(username) > 256:
            msg = "Your username is too long."
            msg += " Usernames must be ≤ 256 characters in length."
            errors.append(msg)
        if db.session.query(Profile).filter(Profile.username == username).count():
            errors.append("This username is already in use.")
        if not validate_email(email):
            errors.append("Please try again with a valid email.")
        if db.session.query(Profile).filter(Profile.email == email).count():
            errors.append("An account is already registered with this email.")
        if not validate_password(pwd1):
            errors.append("Please try again with a valid password.")
        if pwd1 != pwd2:
            errors.append("Your passwords don't match.")
        if not errors:
            hashed = pbkdf2_sha256.hash(pwd1)
            profile = Profile(
                username=username, email=email, password=hashed
            )
            db.session.add(profile)
            db.session.commit()
            return jsonify({'username': profile.username}), 201

    context = {"errors": errors}
    return jsonify(context), 200


@app.route('/api/v1/tasks/', methods=['GET', 'POST'])
@auth.login_required
def all_tasks():
    """A list of all the tasks."""
    return ""


@app.route('/api/v1/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def single_task(id):
    """."""
    return ""


@app.route('/api/v1/accounts/<user_name>', methods=['GET', 'POST'])
@auth.login_required
def profile(user_name):
    """."""
    return ""


def validate_email(email):
    """Ensure that a given email actually looks like an email."""
    is_valid = False
    if len(email) < 256:
        pattern = re.compile('[\w]+@[\w]+\.[a-zA-Z]+')
        matches = pattern.search(pattern)
        if len(matches.group()) == len(email):
            is_valid = True
    return is_valid


def validate_password(pwd):
    """Make sure that a given password meets criteria.

    At least 8 characters.
    No more than 20 characters.
    a-z, A-Z, 0-9, -_!?@#$+
    """
    is_valid = False
    if len(pwd) >= 8 and len(pwd) <= 24:
        pattern = re.compile('[\w@\-\!\?#\$\+]+')
        matches = pattern.search(pwd)
        if len(matches.group()) == len(pwd):
            is_valid = True
    return is_valid


@auth.verify_password
def validate_credentials(username, password):
    """Take in a username, password, and return whether the combo works."""
    is_valid = False
    user = db.session.query(Profile).filter_by(username=username).first()
    if user:
        is_valid = pbkdf2_sha256.verify(password, user.password)
        if is_valid:
            g.user = user
    return is_valid

if __name__ == '__main__':
    app.run()
