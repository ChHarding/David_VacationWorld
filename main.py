
from dotenv import load_dotenv
from urllib.parse import urlencode
from flask import Flask, request, render_template, session, url_for, redirect
from flask_session import Session
import json

import os
load_dotenv()

app = Flask("Trip Pin")

MAPBOX_API_KEY = os.getenv("MAPBOX_API")

app.secret_key = 'your_secret_key'  # Set the secret key to sign the session cookies

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
app.config['SESSION_PERMANENT'] = False
Session(app)

@app.route("/")  
def main_page():
    html_str = render_template('index.html', title="Trip Pin", MAPBOX_API_KEY = MAPBOX_API_KEY) # title will be inlined in {{ title }}
    return html_str  # give it to the browser to display the inline page


@app.errorhandler(500)
def page_not_found(error):
    print(error) 
    s = "Error with " + str(request.args["URL"]) + "<br>" + str(error)   
    s = s + "<br>Hit the Back button and try something else ...)"
    return s

from flask import jsonify

# ... existing imports and setup ...

@app.route("/save_itinerary", methods=['POST'])
def save_itinerary():
    itinerary = request.json
    # Here you would typically save the itinerary to a database
    # For now, we'll just store it in the session
    session['itinerary'] = itinerary
    return jsonify({"status": "success"})

@app.route("/load_itinerary")
def load_itinerary():
    # Here you would typically load the itinerary from a database
    # For now, we'll just retrieve it from the session
    itinerary = session.get('itinerary', [])
    return jsonify(itinerary)


"""code to start server"""
from socket import gethostname
if 'liveweb' not in gethostname(): # all pythonanywhere servers have liveweb in their name
    app.run(debug=False, port=8081)