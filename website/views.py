from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from flask_session import Session
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
    """if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401
    """
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Itinerary name is required"}), 400
    
    new_itinerary = Itinerary(name=name, user_id=current_user.id)
    db.session.add(new_itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary created", "id": new_itinerary.id}), 201

@views.route('/itinerary/<int:itinerary_id>', methods=['DELETE'])
def delete_itinerary(itinerary_id):
    itinerary = Itinerary.query.get(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    db.session.delete(itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary deleted"}), 200

@views.route('/itinerary/<int:itinerary_id>', methods=['PUT'])
def edit_itinerary(itinerary_id):
    itinerary = Itinerary.query.get(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    new_name = request.json.get('name')
    if not new_name:
        return jsonify({"error": "New itinerary name is required"}), 400
    
    itinerary.name = new_name
    db.session.commit()
    
    return jsonify({"message": "Itinerary updated", "id": itinerary.id}), 200


