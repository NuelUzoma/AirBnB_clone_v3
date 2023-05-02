#!/usr/bin/python3
"""
Same as State, create a new view for City objects that handles all
default RESTFul API actions: In the file api/v1/views/cities.py
You must use to_dict() to serialize an object into valid JSON
Update api/v1/views/__init__.py to import this new file
"""


from api.v1.views import app_views
from flask import request, abort, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def all_cities_of_a_state(state_id):
    """Retrieves the list of all City objects of a State"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    cities = [city.to_dict() for city in states.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def single_city(city_id):
    """Retieves a city object"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    storage.delete(cities)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create a city object"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    data = request.get_json
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city object"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    data = request.get_json
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(cities, key, value)
    cities.save()
    return jsonify(cities.to_dict()), 200
