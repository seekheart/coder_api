"""
Main app entry point
Mike Tung
"""

from flask import Flask, jsonify, request, abort

import data_engines
import security
import settings

app = Flask(__name__)
coders_engine = data_engines.CoderEngine()
languages_engine = data_engines.LanguageEngine()

@app.route('/')
def test() -> str:
    """
    Confirmation route to ensure app is working

    Returns:
        confirmation message if success else error will be raised
    """
    return 'It works!'


@app.route('/users', methods=['GET'])
@security.authenticate.requires_auth
def users() -> dict:
    """
    Get route for all users

    Returns:
        list of users if success else 404 response is sent
    """

    data = coders_engine.get_all()
    payload = []
    for user in data:
        current_users = {}
        for k, v in user.items():
            if k == '_id':
                continue
            current_users[k] = v
        payload.append(current_users)
    return jsonify(payload)


@app.route('/users', methods=['POST'])
@security.authenticate.requires_auth
def post_users() -> tuple:
    """
    Post route for adding user data

    Returns:
        Confirmation message if success else 400 bad request
    """

    try:
        r = request.get_json()
        data = {
            'username': r['username'],
            'languages': r['languages']
        }
    except ValueError:
        abort(400)

    if coders_engine.get_one(data['username']):
        abort(409)
    try:
        coders_engine.add_one(data)
    except ValueError:
        abort(500)

    for lang in data['languages']:
        if languages_engine.get_one(lang):
            doc = languages_engine.get_one(lang)
            if data['username'] not in doc['users']:
                doc['users'].append(data['username'])
                languages_engine.update_one(lang, doc)
            continue
        else:
            doc = {'name': lang, 'users': [data['username']]}
            languages_engine.add_one(doc)


    return 'Ok', 201


@app.route('/users/<user>', methods=['GET'])
@security.authenticate.requires_auth
def get_one_user(user: str) -> dict:
    """
    Get route for a single user

    Args:
        user: username to query for

    Returns:
        specified user data
    """

    data = coders_engine.get_one(user)
    payload = None
    try:
        payload = {k: v for k, v in data.items() if k != '_id'}
    except AttributeError:
        abort(404)
    return jsonify(payload)


@app.route('/users/<user>', methods=['DELETE'])
@security.authenticate.requires_auth
def delete_one_user(user: str) -> tuple:
    """
    Delete route to remove a user

    Args:
        user: username to search and delete

    Returns:
        status code for either success 204 or failure 400
    """
    if not coders_engine.get_one(user):
        abort(400)
    coders_engine.delete_one(user)
    return '', 204


@app.route('/users/<user>', methods=['PATCH'])
@security.authenticate.requires_auth
def edit_one_user(user: str) -> tuple:
    """
    Patch route to edit a user's data

    Args:
        user: user to search for and edit

    Returns:
        update message if success else 404 not found or 400 if bad data
    """
    new_data = request.get_json()

    if len(new_data) < 1:
        abort(400)
    try:
        coders_engine.update_one(user, new_data)
    except ValueError:
        abort(404)

    return '', 204



@app.route('/languages', methods=['GET'])
@security.authenticate.requires_auth
def get_languages() -> dict:
    """
    Get route for all languages

    Returns:
        json language data
    """

    data = languages_engine.get_all()
    payload = []

    for datum in data:
        current_data = {}
        for k, v in datum.items():
            if k == '_id':
                continue
            current_data[k] = v
        payload.append(current_data)
    return jsonify(payload)


@app.route('/languages', methods=['POST'])
@security.authenticate.requires_auth
def add_languages() -> tuple:
    """
    Post route for adding language data

    Returns:
        Confirmation message if success or 400 for failure
    """

    r = request.get_json()

    try:
        data = {
            'name': r['name'],
            'users': r['users']
        }
    except ValueError:
        abort(400)

    if languages_engine.get_one(data['name']):
        abort(409)
    try:
        languages_engine.add_one(data)
    except ValueError:
        abort(500)

    return 'Ok', 201


@app.route('/languages/<language>', methods=['GET'])
@security.authenticate.requires_auth
def get_one_language(language: str) -> dict:
    """
    Get one route for a single language
    Args:
        language: programming language name to search for

    Returns:
        Queried language data in json time
    """

    data = languages_engine.get_one(language)
    payload = {k: v for k, v in data.items() if k != '_id'}
    return jsonify(payload)


@app.route('/languages/<language>', methods=['DELETE'])
@security.authenticate.requires_auth
def delete_one_language(language: str) -> tuple:
    """
    Delete one route for a single language

    Args:
        language: programming language name to search for and delete

    Returns:
        Confirmation message if deleted else 400
    """

    if not languages_engine.get_one(language):
        abort(400)
    languages_engine.delete_one(language)
    return '', 204


@app.route('/languages/<language>', methods=['PATCH'])
@security.authenticate.requires_auth
def edit_one_language(language: str) -> tuple:
    new_data = request.get_json()

    if len(new_data) < 1:
        abort(400)
    try:
        languages_engine.update_one(language, new_data)
    except ValueError:
        abort(404)

    return '', 204


if __name__ == '__main__':
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
        threaded=settings.MULTITHREADING
    )
