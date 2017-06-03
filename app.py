"""
Main app entry point
Mike Tung
"""

from flask import Flask, jsonify, request, abort

import settings
from coder_engine.coder_engine import CoderEngine

app = Flask(__name__)
coders_engine = CoderEngine(settings.MONGO_HOST,
                            settings.MONGO_PORT,
                            settings.MONGO_DB,
                            settings.MONGO_COLLECTIONS
                            )
languages_engine = CoderEngine(settings.MONGO_HOST,
                               settings.MONGO_PORT,
                               settings.MONGO_DB,
                               settings.MONGO_COLLECTIONS
                               )


@app.route('/')
def test() -> str:
    """
    Confirmation route to ensure app is working

    Returns:
        confirmation message if success else error will be raised
    """
    return 'It works!'


@app.route('/users', methods=['GET'])
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
def post_users() -> dict:
    """
    Post route for adding user data

    Returns:
        Confirmation message if success else 400 bad request
    """
    data = request.get_json()
    try:
        user_name = data['username']
        languages = data['languages']
        coders_engine.add_one(user_name, languages)
    except KeyError as e:
        abort(400)

    return jsonify({'success': True})


@app.route('/users/<user>', methods=['GET'])
def get_one_user(user: str) -> dict:
    """
    Get route for a single user

    Args:
        user: username to query for

    Returns:
        specified user data
    """
    data = coders_engine.get_one(user)
    try:
        payload = {k: v for k, v in data.items() if k != '_id'}
    except AttributeError as e:
        abort(404)
    return jsonify(payload)


@app.route('/users/<user>', methods=['DELETE'])
def delete_one_user(user: str) -> dict:
    """
    Delete route to remove a user

    Args:
        user: username to search and delete

    Returns:
        delete message if success else 400 bad request
    """
    if not coders_engine.get_one(user):
        abort(400)
    coders_engine.delete_one(user)
    return jsonify({'deleted': True})


@app.route('/users/<user>', methods=['PATCH'])
def edit_one_user(user: dict) -> dict:
    """
    Patch route to edit a user's data

    Args:
        user: user to search for and edit

    Returns:
        update message if success else 404 not found or 400 if bad data
    """
    new_data = request.get_json()

    if len(new_data.keys()) < 1:
        abort(400)
    try:
        coders_engine.update_one(user, new_data)
    except ValueError as e:
        abort(404)

    return jsonify({'updated': True})


@app.route('/languages', methods=['GET'])
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
def add_languages() -> dict:
    """
    Post route for adding language data

    Returns:
        Confirmation message if success or 400 for failure
    """
    data = request.get_json()
    lang_name = ''
    lang_users = ''

    if len(data.keys()) < 1:
        abort(400)
    try:
        lang_name = data['name']
        lang_users = data['users']
    except KeyError as e:
        abort(400)

    languages_engine.add_one(lang_name, lang_users)
    return jsonify({'success': True})


@app.route('/languages/<language>', methods=['GET'])
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
def delete_one_language(language: str) -> dict:
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
    return jsonify({'deleted': True})


@app.route('/languages/<language>', methods=['PATCH'])
def edit_one_language(language: str) -> dict:
    new_data = request.get_json()
    languages_engine.update_one(language, new_data)
    return jsonify({'updated': True})


if __name__ == '__main__':
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
        threaded=settings.MULTITHREADING
    )
