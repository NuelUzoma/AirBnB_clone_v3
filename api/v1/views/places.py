#!/usr/bin/python3
"""
Create a file places.py, that handles all default RestFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all Place objects"""
    places = storage.get(City, city_id)
    if places is None:
        abort(404)
    places_all = storage.all(Place).values()
    list_places_city_id = list(map(lambda place: place.city_id == city_id,
                           places_all))
    list_places = list(map(lambda place: place.to_dict(),
                           list_places_city_id))
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def single_place(place_id):
    """Retrieves a Place object"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    return jsonify(places.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place Object"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    else:
        storage.delete(places)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place object"""
    places = storage.get(City, city_id)
    if places is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'user_id' not in data.keys():
        abort(400, description='Missing user_id')
    if 'name' not in data.keys():
        abort(400, description='Missing name')
    user_id = data['user_id']
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    data.city_id = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in [
            'id',
            'user_id',
            'city_id',
            'created_at',
            'updated_at'
        ]:
            setattr(places, key, value)
    places.save()
    return jsonify(places.to_dict()), 200
