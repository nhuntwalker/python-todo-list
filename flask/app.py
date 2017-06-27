"""."""
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(
    os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Task


@app.route('/')
def home_view():
    """."""
    response = app.response_class(
        response=json.dumps({'page': 'home_page'}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/tasks', methods=['GET', 'POST'])
def all_tasks():
    """."""
    return ""


@app.route('/tasks/<id>', methods=['GET', 'PUT', 'DELETE'])
def single_task(id):
    """."""
    return ""


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


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """."""
    return ""


if __name__ == '__main__':
    app.run()
