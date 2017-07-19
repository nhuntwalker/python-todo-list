# from app import app as create_app
# import pytest


# @pytest.fixture
# def app():
#     test_it = create_app()
#     return test_it


# @pytest.fixture
# def app_client(app):
#     client = app.test_client()
#     return client


# def test_home_view_returns_json(app_client):
#     """."""
#     res = app_client.get("/")
#     assert res.status_code == 200
