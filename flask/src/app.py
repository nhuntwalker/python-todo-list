"""."""
from datetime import datetime, timedelta
from flask import (
    Blueprint, Flask, jsonify, request
)
from flask_sqlalchemy import SQLAlchemy
import jwt
import os
from passlib.hash import pbkdf2_sha256
import re


app = Flask(__name__)
app.config.from_object(
    os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

auth_blueprint = Blueprint('auth', __name__)
app.register_blueprint(auth_blueprint)

# from models import Task, Profile

# MODELS


class Task(db.Model):
    """The Task model."""

    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(length=256, convert_unicode=True), nullable=False
    )
    due_date = db.Column(db.DateTime())
    complete = db.Column(db.Boolean())
    profile = db.relationship('Profile', back_populates='tasks')
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __init__(self, title, category=None, due_date=None, complete=False):
        """Construct a new Task."""
        self.title = title
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
        db.String(length=256),
        nullable=False
    )
    tasks = db.relationship('Task', back_populates='profile')

    def __init__(self, username=None, email=None, password=None):
        """Construct a new user profile."""
        self.username = username
        self.email = email
        self.password = password

    def encode_auth_token(self):
        """Generate the auth token for this profile."""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=30),
                'iat': datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload, app.config.get('SECRET_KEY'), algorithm='HS256'
            )
        except Exception as e:
            return e

    def to_json(self):
        """Return a JSON representation of a given profile."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    @staticmethod
    def decode_auth_token(auth_token):
        """Given an auth token, decode the auth token and check."""
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        """String representation."""
        fill_string = '<{} id:{} email:{}>'
        return fill_string.format(
            self.username, self.id, self.email
        )


db.Index('usernames', Profile.username, unique=True)
db.Index('user_emails', Profile.email, unique=True)

# VIEWS


@app.route('/api/v1/')
def home_view():
    """The home page for the to do list app."""
    pass


@app.route('/api/v1/tasks/', methods=['GET', 'POST'])
def all_tasks():
    """A list of all the tasks."""
    pass


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

        profile = db.session.query(Profile).filter_by(username=username).one_or_none()
        if not profile or not pbkdf2_sha256.verify(password, profile.password):
            msg = "The username or password provided is incorrect. "
            msg += "Please try again."
            errors.append(msg)

        if not errors:
            auth_token = profile.encode_auth_token()
            if auth_token:
                response_context = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return jsonify(response_context), 200

    context["errors"] = errors
    return jsonify(context), 200


auth_blueprint.add_url_rule(
    '/api/v1/login',
    view_func=login,
    methods=['GET', 'POST']
)


@app.route('/api/v1/logout')
def logout():
    """Remove authentication from the request."""
    pass


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
        if db.session.query(Profile).filter(
            Profile.username == username
        ).count():
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

            auth_token = profile.encode_auth_token()
            response_context = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return jsonify(response_context), 201

    context = {"errors": errors}
    return jsonify(context), 200


auth_blueprint.add_url_rule(
    '/api/v1/register',
    view_func=register,
    methods=['GET', 'POST']
)


@app.route('/api/v1/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def single_task(id):
    """Detail for an individual task."""
    pass


@app.route('/api/v1/profile', methods=['GET', 'POST'])
def profile():
    """."""

    auth_token = request.headers.get('Authorization')
    if request.method == "GET":
        if auth_token:
            auth_id = Profile.decode_auth_token(auth_token)
            import pdb; pdb.set_trace()
            if not isinstance(auth_id, str):
                profile = db.session.query(Profile).get(auth_id)
                response_context = {
                    'status': 'success',
                    'data': profile.to_json()
                }
                return jsonify(response_context), 200
        else:
            response_context = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return jsonify(response_context), 401

auth_blueprint.add_url_rule(
    '/api/v1/profile',
    view_func=profile,
    methods=['GET', 'POST']
)


def validate_email(email):
    """Ensure that a given email actually looks like an email."""
    is_valid = False
    if len(email) < 256:
        pattern = re.compile('[\w]+@[\w]+\.[a-zA-Z]+')
        matches = pattern.search(email)
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

if __name__ == '__main__':
    app.run()
