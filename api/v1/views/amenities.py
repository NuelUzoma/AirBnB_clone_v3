#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles all
default RESTFul API actions: In the file api/v1/views/amenities.py
You must use to_dict() to serialize an object into valid JSON
Update api/v1/views/__init__.py to import this new file
"""


from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def all_amenities():
    """Retrieve the list of all amenity objects"""
    amenities = storage.all(Amenity).values()
    amenitys = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenitys)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def single_amenity(amenity_id):
    """Retrieve a amenity object"""
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    return jsonify(amenities.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a amenity object"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Create a amenity object"""
    data = request.get_json
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
