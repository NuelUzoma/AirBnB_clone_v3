#!/usr/bin/python3
"""
Creates a new view for Review objects that handles
all default RESTFul API action
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """Retrieves the list of all Review objects"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    else:
        reviews = places.reviews
        list_reviews = list(map(lambda review: review.to_dict(), reviews))
        return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def single_review(review_id):
    """Retrieves a Review object"""
    reviews = storage.get(Review, review_id)
    if reviews is None:
        abort(404)
    return jsonify(reviews.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews(review_id):
    """Deletes a Review object"""
    reviews = storage.get(Review, review_id)
    if reviews is None:
        abort(404)
    else:
        storage.delete(reviews)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a Review object"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    if 'text' not in data:
        abort(400, description='Missing text')
    user_id = data['user_id']
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review object"""
    reviews = storage.get(Review, review_id)
    if reviews is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in [
            'id',
            'user_id',
            'place_id',
            'created_at',
            'updated_at'
        ]:
            setattr(reviews, key, value)
    reviews.save()
    return jsonify(reviews.to_dict()), 200
