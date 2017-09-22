# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app import app, db


@app.route("/")
def home():
    """Return the home page."""
    pass


@app.route("/api/v1/")
def info():
    """Information about the API and existing endpoints."""
    pass


@app.route("/api/v1/tasks", methods=["GET", "POST"])
def tasks():
    """List all tasks or add a new one."""
    pass


@app.route("/api/v1/tasks/<id>", methods=["GET", "PUT", "DELETE"])
def one_task(id):
    """Get, update, or delete one task by ID."""
    pass


@app.route("/api/v1/profiles", methods=["POST"])
def profiles():
    """Add a new user profile."""
    pass


@app.route("/api/v1/profiles/<id>", methods=["GET", "PUT", "DELETE"])
def one_profile(id):
    """Get, update, or delete a user profile by ID."""
    pass
