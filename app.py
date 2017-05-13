"""
Main app entry point
Mike Tung
"""

from flask import Flask, jsonify, request

from coder_engine.coder_engine import CoderEngine
from settings import *

app = Flask(__name__)
data_engine = CoderEngine(MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION)


@app.route('/')
def test():
    return 'It works!'


@app.route('/users', methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        data = data_engine.get_all_users()
        payload = []
        current_user = {}
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
        user_name = data['username']
        languages = data['languages']
        data_engine.add_user(user_name, languages)
        return 'Success!', 201


@app.route('/users/<user>', methods=['GET'])
def get_one_user(user):
    if request.method == 'GET':
        data = data_engine.get_user(user)
        payload = {k: v for k, v in data.items() if k != '_id'}
        return jsonify(payload)


# def main():
#     data_engine = CoderEngine('localhost', 27017, 'coder', 'users')
#
#
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
