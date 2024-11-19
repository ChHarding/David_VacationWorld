from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlencode
from flask import Flask, request, render_template, session, url_for, redirect, jsonify, flash
from flask_session import Session
from datetime import timedelta
import json

import os
load_dotenv()

app = Flask("Trip Pin")
app.permanent_session_lifetime = timedelta(days=5)
MAPBOX_API_KEY = os.getenv("MAPBOX_API")

app.secret_key = 'your_secret_key'  # Set the secret key to sign the session cookies

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
app.config['SESSION_PERMANENT'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

Session(app)

db = SQLAlchemy(app)

@app.errorhandler(500)
def page_not_found(error):
    print(error) 
    s = "Error with " + str(request.args["URL"]) + "<br>" + str(error)   
    s = s + "<br>Hit the Back button and try something else ...)"
    return s



@app.route('/itinerary', methods=['POST'])
def create_itinerary():
    """if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401
    """
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Itinerary name is required"}), 400
    
    new_itinerary = Itinerary(name=name)
    db.session.add(new_itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary created", "id": new_itinerary.id}), 201

@app.route('/itinerary/<int:itinerary_id>', methods=['DELETE'])
def delete_itinerary(itinerary_id):
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    itinerary = Itinerary.query.get(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    db.session.delete(itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary deleted"}), 200

@app.route('/itinerary/<int:itinerary_id>', methods=['PUT'])
def edit_itinerary(itinerary_id):
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    itinerary = Itinerary.query.get(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    new_name = request.json.get('name')
    if not new_name:
        return jsonify({"error": "New itinerary name is required"}), 400
    
    itinerary.name = new_name
    db.session.commit()
    
    return jsonify({"message": "Itinerary updated", "id": itinerary.id}), 200


