"""."""
from flask import Flask, json, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import re


app = Flask(__name__)
app.config.from_object(
    os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Task


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
    """."""
    return ""


@app.route('/tasks', methods=['GET', 'POST'])
def all_tasks():
    """A list of all the tasks """
    return ""


@app.route('/tasks/<id>', methods=['GET', 'PUT', 'DELETE'])
def single_task(id):
    """."""
    return ""


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """."""
    return ""


def _validate_email(email):
    """Ensure that a given email actually looks like an email."""
    is_valid = False
    pass


def _validate_password(pwd):
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
