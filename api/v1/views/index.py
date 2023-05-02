#!/usr/bin/python3
"""
create a file index.py
import app_views from api.v1.views
create a route /status on the object
app_views that returns a JSON: "status": "OK
"""


from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """return a JSON format of the HTTP Response"""
    return jsonify({'status': 'OK'})
