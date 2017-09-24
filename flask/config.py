# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
TEST_DATABASE_URI = os.environ.get('TEST_DB_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False