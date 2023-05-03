#!/usr/bin/python3
"""
Creates a new view for User objects that handles all default
RESTFul API actions. In the file api/v1/views/users.py,
you must use to_dict() to retrieve an object into a valid JSON.
"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """Retrieve list of all user objects"""
    users = storage.all(User).values()
    list_users = list(map(lambda user: user.to_dict(), users))
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def single_user(user_id):
    """Retrieve a user object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    else:
        return jsonify(users.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a user object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    else:
        storage.delete(users)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    """Create a user object"""
    data = request.get_json
    if not data:
        abort(400, description='Not a JSON')
    if 'email' not in data:
        abort(400, desription='Missing email')
    if 'password' not in data:
        abort(400, description='Missing password')
    user = User(**data)
    storage.new(user)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a user object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    else:
        data = request.get_json
        if not data:
            abort(400, description='Not in JSON')
        for key in data.keys():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(users, key, data[key])
        users.save()
        return jsonify(users.to_dict()), 200
