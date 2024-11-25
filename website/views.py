from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from .models import User, Itinerary, Place
from . import db
import json
from dotenv import load_dotenv
import os
load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_API")

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def main_page():
    if request.method == 'POST': 
        data = request.form.get('data')
    html_str = render_template('main_page.html', title="Trip Pin", MAPBOX_API_KEY = MAPBOX_API_KEY) # title will be inlined in {{ title }}
    return html_str

@views.route("/save_itinerary", methods=['POST'])
def save_itinerary():
    itinerary = request.json
    # Here you would typically save the itinerary to a database
    # For now, we'll just store it in the session
    session['itinerary'] = itinerary
    return jsonify({"status": "success"})

@views.route("/load_itinerary")
def load_itinerary():
    # Here you would typically load the itinerary from a database
    # For now, we'll just retrieve it from the session
    itinerary = session.get('itinerary', [])
    return jsonify(itinerary)


@views.route('/itinerary', methods=['POST'])
def create_itinerary():
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Itinerary name is required"}), 400
    
    new_itinerary = Itinerary(name=name, user_id=current_user.id)
    db.session.add(new_itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary created", "id": new_itinerary.id}), 201

@views.route('/itinerary/<itinerary_id>', methods=['DELETE'])
def delete_itinerary(itinerary_id):
    itinerary = Itinerary.query.get(itinerary_id)
    
    if not itinerary:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    db.session.delete(itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary deleted"}), 200

@views.route('/itinerary/<itinerary_id>', methods=['PUT'])
def edit_itinerary(itinerary_id):
    itinerary = Itinerary.query.get(itinerary_id)
    if not itinerary:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    new_name = request.json.get('name')

    itinerary.name = new_name
    db.session.commit()
    
    return jsonify({"message": "Itinerary updated", "id": itinerary.id}), 200


@views.route('/places', methods=['GET','POST'])
def create_place():
    if request.method == 'GET':
        data = request.form.get('places')
    data = request.json
    name = data.get('name')
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    if not name:
        return jsonify({"error": "Place name is required"}), 400
    
    if not name or longitude is None or latitude is None:
        return jsonify({"error": "Place name and coordinates are required"}), 400

    new_place = Place(
        name=name,
        longitude=longitude,
        latitude=latitude,
        user_id=current_user.id,
    )
    
    db.session.add(new_place)
    db.session.commit()
    
    return jsonify({"message": "Place created", "id": new_place.id}), 201

@views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = Place.query.get(place_id)
    
    if not place:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    db.session.delete(place)
    db.session.commit()
    
    return jsonify({"message": "Place deleted"}), 200

@views.route('/places/<place_id>', methods=['PUT'])
def edit_place(place_id):
    place = Place.query.get(place_id)
    if not place or place.user_id != current_user.id:
        return jsonify({"error": "Place not found or unauthorized"}), 404

    new_name = request.json.get('name')
    if new_name:
        place.name = new_name
    
    # Optionally update other fields like longitude and latitude if needed
    new_longitude = request.json.get('longitude')
    new_latitude = request.json.get('latitude')
    
    if new_longitude is not None:
        place.longitude = new_longitude
    if new_latitude is not None:
        place.latitude = new_latitude

    db.session.commit()
    return jsonify({"message": "Place updated", "id": place.id}), 200