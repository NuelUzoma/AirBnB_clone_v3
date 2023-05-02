#!/usr/bin/python3
"""
create a file index.py
import app_views from api.v1.views
create a route /status on the object
app_views that returns a JSON: "status": "OK
"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """return a JSON format of the HTTP Response"""
    return jsonify({'status': 'OK'})


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """create an endpoint that retrieves the number of each objects by type"""
    from models import storage
    storage.count()
