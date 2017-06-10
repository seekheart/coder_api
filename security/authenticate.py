import functools

import flask

import settings


def check_credentials(username, pw):
    """Checks if username and passwords match"""
    return username == settings.API_USER and pw == settings.API_PW


def not_authorized():
    """Sends 401 response to bad authenticate"""
    return flask.Response('Unauthorized Access!', 401)


def requires_auth(func):
    """Wraps a route with authorization"""

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        auth = flask.request.authorization
        if not auth or not check_credentials(auth.username, auth.password):
            return not_authorized()
        return func(*args, **kwargs)

    return decorated
