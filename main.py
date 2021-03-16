# Simple python tool to parse parking lot data and provide it via REST API
# requires (via pip3 install): flask, beautifulsoup4, requests
import flask
from flask import request, jsonify
from bs4 import BeautifulSoup
import requests


# this funtion contains all the stuff to fetch and parse the info from the website
# will return an array of dicts
def fetch_and_parse():
    # fetch html file
    html_text = requests.get("https://www.heilbronn.de/allgemeine-inhalte/ajax-parkhausbelegung.html?type=1496993343").text
    # init with BeautifulSoup
    soup = BeautifulSoup(html_text, "html.parser")

    # parse the timestamp and transform
    timestamp = soup.find(class_="col-sm-12").text
    timestamp = timestamp.replace('Datum: ','').replace('Uhrzeit: ','')

    # get tags with content
    garages_raw = soup.find_all(class_="row carparkContent")

    # go through the content tags and extract the data
    id = 0
    garages = []
    for garage_raw in garages_raw:
        # step by step parsing the details into a list
        # order: name, entrance, number of free lots

        #get name and entrance info
        name_n_entrance=garage_raw.find(class_="carparkLocation col-sm-9").text
        details = name_n_entrance.split("Zufahrt: ",2)
        if len(details) < 2:    # if there is no entrance given, a "-"
            details.append("-")
        
        # get number of free lots
        details.append(garage_raw.find(class_="col-sm-5").text.replace("Freie Parkplätze: ",""))
        
        # create a dictionary from the data, cut of leading/trailing spaces, \t and \n
        garages.append(
            {'id': id,
            'name': details[0].replace('\t', '').replace('\n', '').strip(),
            'entrance': details[1].replace('\t', '').replace('\n', '').strip(),
            'free_lots': details[2].replace('\t', '').replace('\n', '').strip(),
            'timestamp': timestamp}
        )
        id+=1
    
    return garages

# init and start the server
def init_server():
    # initialize the REST server using flask
    server = flask.Flask(__name__)
    server.config["DEBUG"] = True

    # create the reachable resources of the server using the array of dicts parsed
    # welcome page
    @server.route('/', methods=['GET'])
    def home():
        return '''<h1>Parking API</h1>
    <p>Prototype API free parking lots in garages in Heilbronn, Germany.</p>'''

    # all garages
    @server.route('/api/v1/resources/garages/all', methods=['GET'])
    def api_all():
        data = fetch_and_parse()
        return jsonify(data)

    # garage selection per id
    @server.route('/api/v1/resources/garages', methods=['GET'])
    def api_id():
        data = fetch_and_parse()
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
        for garage in data:
            if garage['id'] == id:
                results.append(garage)

        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(results)
    
    # start our little server
    server.run()

init_server()
