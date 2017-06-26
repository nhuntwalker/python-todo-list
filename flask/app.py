"""."""
from flask import Flask
import os


app = Flask(__name__)
app.config.from_object(
    os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig')
)


@app.route('/')
def home_view():
    """."""
    return "Just a test"


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
