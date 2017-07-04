"""."""
from flask import Flask, json, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import re
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.config.from_object(
    os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Task, Profile


@app.route('/')
def home_view():
    """The home page for the to do list app."""
    context = {
        'title': 'Python To Do | Home',
        'login': url_for('login'),
        'register': url_for('register'),
        'settings': url_for('settings')
    }
    response = app.response_class(
        response=json.dumps(context),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    """."""
    return ""


@app.route('/logout')
def logout():
    """."""
    return ""


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Create a new user with email and password."""
    errors = []
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        pwd1 = request.form['password']
        pwd2 = request.form['password2']
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
            return redirect(url_for('all_tasks'))

    context = {"errors": errors}
    response = app.response_class(
        response=json.dumps(context),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/tasks', methods=['GET', 'POST'])
def all_tasks():
    """A list of all the tasks."""
    return ""


@app.route('/tasks/<id>', methods=['GET', 'PUT', 'DELETE'])
def single_task(id):
    """."""
    return ""


@app.route('/settings', methods=['GET', 'POST'])
def settings():
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

if __name__ == '__main__':
    app.run()
