"""
Main app entry point
Mike Tung
"""

from flask import Flask, jsonify, request, abort

from coder_engine.coder_engine import CoderEngine
from settings import *

app = Flask(__name__)
coders_engine = CoderEngine(MONGO_HOST,
                            MONGO_PORT,
                            MONGO_DB,
                            MONGO_USER_COLLECTION
                            )
languages_engine = CoderEngine(MONGO_HOST,
                               MONGO_PORT,
                               MONGO_DB,
                               MONGO_LANGUAGES_COLLECTION
                               )


@app.route('/')
def test():
    return 'It works!'


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        data = coders_engine.get_all()
        payload = []
        for user in data:
            current_user = {}
            for k, v in user.items():
                if k == '_id':
                    continue
                current_user[k] = v
            payload.append(current_user)
        return jsonify(payload)
    elif request.method == 'POST':
        data = request.get_json()
        try:
            user_name = data['username']
            languages = data['languages']
            coders_engine.add_one(user_name, languages)
        except KeyError as e:
            abort(400)

        return 'Success!'


@app.route('/users/<user>', methods=['GET', 'DELETE', 'PATCH'])
def one_user(user):
    if request.method == 'GET':
        data = coders_engine.get_one(user)
        try:
            payload = {k: v for k, v in data.items() if k != '_id'}
        except AttributeError as e:
            abort(400)
        return jsonify(payload)
    elif request.method == 'DELETE':
        if not coders_engine.get_one(user):
            abort(400)
        coders_engine.delete_one(user)
        return jsonify({'deleted': True})
    elif request.method == 'PATCH':
        new_data = request.get_json()
        coders_engine.update_one(user, new_data)
        return jsonify({'updated': True})


@app.route('/languages', methods=['GET', 'POST'])
def languages():
    if request.method == 'GET':
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
    elif request.method == 'POST':
        data = request.get_json()
        try:
            lang_name = data['name']
            users = data['users']
        except KeyError as e:
            abort(400)
        languages_engine.add_one(lang_name, users)
        return 'Success!', 201


@app.route('/languages/<language>', methods=['GET', 'DELETE', 'PATCH'])
def one_language(language):
    if request.method == 'GET':
        data = languages_engine.get_one(language)
        payload = {k: v for k, v in data.items() if k != '_id'}
        return jsonify(payload)
    elif request.method == 'DELETE':
        if not languages_engine.get_one(language):
            abort(400)
        languages_engine.delete_one(language)
        return jsonify({'deleted': True})
    elif request.method == 'PATCH':
        new_data = request.get_json()
        languages_engine.update_one(language, new_data)
        return jsonify({'updated': True})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
