#!/usr/bin/python3
"""
Create a folder api at the root of the project directory with __init__.py
Create a folder v1 inside the api folder with __init__.py
This will be the api for the application
"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
resources = {
    "/*": {
        "origins": "0.0.0.0"
    }
}
CORS(app, resources=resources)


@app.teardown_appcontext
def teardown(exception):
    """Calling the storage.close() function"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """Error handler to return a JSON-formatted 404 status code response"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
