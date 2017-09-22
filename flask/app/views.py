# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app import app, db


@app.route("/")
@app.route("/api/v1/")
@app.route("/api/v1/tasks", methods=["GET", "POST"])
@app.route("/api/v1/tasks/<id>", methods=["GET", "PUT", "DELETE"])
@app.route("/api/v1/profiles", methods=["POST"])
@app.route("/api/v1/profiles/<id>", methods=["GET", "PUT", "DELETE"])
