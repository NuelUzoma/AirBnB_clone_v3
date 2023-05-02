#!/usr/bin/python3
"""
create a variable app, instance of Flask import storage from models
import app_views from api.v1.views register the blueprint
app_views to your Flask instance app declare a method
to handle @app.teardown_appcontext that calls storage.close()
inside if __name__ == "__main__":, run your Flask server
(variable app) with:
host = environment variable HBNB_API_HOST or 0.0.0.0 if not defined
port = environment variable HBNB_API_PORT or 5000 if not defined
threaded=True
"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


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
