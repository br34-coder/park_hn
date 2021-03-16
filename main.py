# Simple python tool to parse parking lot data and provide it via REST API
import flask
from flask import request, jsonify

# initialize the REST server using flask
server = flask.Flask(__name__)
server.config["DEBUG"] = True

# Some static test data. Later we will use data from https://www.heilbronn.de/allgemeine-inhalte/ajax-parkhausbelegung.html?type=1496993343
garages = [
    {'id': 0,
     'name': 'Am Bollwerksturm',
     'entrance': 'Mannheimer Straße 25',
     'free_lots': '202',
     'timestamp': '2018-11-18 09:32:36.435350'},
    {'id': 1,
     'name': 'City-Parkhaus Experimenta',
     'entrance': ' ',
     'free_lots': '876',
     'timestamp': '2018-11-18 09:32:36.435350'},
    {'id': 2,
     'name': 'Harmonie',
     'entrance': 'Gymnasiumstraße',
     'free_lots': '372',
     'timestamp': '2018-11-18 09:32:36.435350'},
]

# create the reachable resources of the server
# welcome page
@server.route('/', methods=['GET'])
def home():
    return '''<h1>Parking API</h1>
<p>Prototype API free parking lots in garages in Heilbronn, Germany.</p>'''

# all garages
@server.route('/api/v1/resources/garages/all', methods=['GET'])
def api_all():
    return jsonify(garages)

# garage selection per id
@server.route('/api/v1/resources/garages', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for garage in garages:
        if garage['id'] == id:
            results.append(garage)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

# start our little server
server.run()
