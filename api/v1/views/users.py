#!/usr/bin/python3
"""
Create a new user for User Onject that handles all default RESTFul API
actions: In the file 'api/v1/views/users.py' You must use to_dict() to
retrieve an object into a valid JSON. Update api/v1/views/__init__.py
to import this new file It has 5 endpoints: Retrieves the list of all
User objects: GET /api/v1/users
"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users/', method=['GET'])
def get_all_users():
    """Retrieve list of all user objects"""
    users = storage.all(User).values()
    list_users = [user.to_dict() for user in users]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def single_user(user_id):
    """Retrieve a user object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    storage.delete()
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
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a user object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    data = request.get_json
    if not data:
        abort(400, description='Not in JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(users, key, value)
    users.save()
    return jsonify(users.to_dict()), 200
