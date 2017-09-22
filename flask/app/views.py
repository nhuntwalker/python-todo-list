# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app import app, db
from flask import jsonify


@app.route("/")
def home():
    """Return the home page."""
    data = {
        "title": "Home"
    }
    return jsonify(data)


@app.route("/api/v1/")
def info():
    """Information about the API and existing endpoints."""
    data = {
        "API information": {
            "methods": ["GET"],
            "uri": "/api/v1/"
        },
        "List/add tasks": {
            "methods": ["GET", "POST"],
            "uri": "/api/v1/tasks"
        },
        "Read/modify tasks": {
            "methods": ["GET", "PUT", "DELETE"],
            "uri": "/api/v1/tasks/<int:id>"
        },
        "Create user profile": {
            "methods": ["POST"],
            "uri": "/api/v1/profiles"
        },
        "Read/modify user profile": {
            "methods": ["GET", "PUT", "DELETE"],
            "uri": "/api/v1/profiles/<int:id>"
        }
    }
    return jsonify(data)


@app.route("/api/v1/tasks", methods=["GET", "POST"])
def tasks():
    """List all tasks or add a new one."""
    pass


@app.route("/api/v1/tasks/<int:id>", methods=["GET", "PUT", "DELETE"])
def one_task(id):
    """Get, update, or delete one task by ID."""
    pass


@app.route("/api/v1/profiles", methods=["POST"])
def create_profile():
    """Add a new user profile."""
    pass


@app.route("/api/v1/profiles/<int:id>", methods=["GET", "PUT", "DELETE"])
def one_profile(id):
    """Get, update, or delete a user profile by ID."""
    pass


@app.route("/api/v1/login", methods=["POST"])
def login():
    """Authenticate a user."""
    pass


@app.route("/api/v1/logout")
def logout():
    """Unauthenticate a user."""
    pass
