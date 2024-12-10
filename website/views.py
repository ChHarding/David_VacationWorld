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


@views.route('/', methods=['GET'])
@login_required
def main_page():
    '''
    Main function to render the main page of the website 
    Returns:
        html string: the main page of the website
    '''
    html_str = render_template('main_page.html', title="Trip Pin", MAPBOX_API_KEY = MAPBOX_API_KEY) # title will be inlined in {{ title }}
    return html_str

@views.route('/itinerary', methods=['GET','POST'])
def create_itinerary():
    """
    Handle the creation and retrieval of itineraries for the current user.
    GET:
        Retrieve all itineraries for the current user.
        Returns:
            JSON response containing a list of itineraries with their details.
    POST:
        Create a new itinerary for the current user.
        Request JSON body:
            - name (str): The name of the itinerary.
        Returns:
            JSON response with a success message and the ID of the created itinerary if successful.
            JSON response with an error message if the itinerary name is missing or already exists.
    """
    if request.method == 'GET':
        itineraries = Itinerary.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            "id": itinerary.id,
            "name": itinerary.name,
            "place": [{
                "id": place.id,
                "name": place.name,
                "longitude": place.longitude,
                "latitude": place.latitude,
                "rating": place.rating,
                "review": place.review
            } for place in itinerary.places]
        } for itinerary in itineraries])
    name = request.json.get('name')
    if not name:
        return jsonify({"error": "Itinerary name is required"}), 400
    
    itinerary_exists = db.session.query(Itinerary).filter_by(name=name, user_id=current_user.id).first()
    if itinerary_exists:
        return jsonify({"error": "Itinerary already exists"}), 404
    else:
        new_itinerary = Itinerary(name=name, user_id=current_user.id)
        db.session.add(new_itinerary)
        db.session.commit()
        return jsonify({"message": "Itinerary created", "id": new_itinerary.id}), 201

@views.route('/itinerary/<itinerary_name>', methods=['POST'])
def add_pins_to_itinerary(itinerary_name):
    """
    Add a pin to an itinerary.
    This route handles the addition of a pin (place) to a user's itinerary.
    It expects a JSON payload with a 'placeId' key.
    Args:
        itinerary_name (str): The name of the itinerary to which the pin will be added.
    Returns:
        Response: A JSON response indicating success or failure.
            - On success: {"message": "Pins added to itinerary", "id": itinerary.id}, 200
            - If itinerary not found or unauthorized: {"error": "Itinerary not found or unauthorized"}, 404
            - If pin not found: {"error": "Pin not found"}, 404
    """    
    itinerary = Itinerary.query.filter_by(name=itinerary_name, user_id=current_user.id).first()
    if itinerary == None:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    placeId = request.json.get('placeId')
    place = Place.query.get(placeId)
    if not place:
        return jsonify({"error": "Pin not found"}), 404
    itinerary.places.append(place)
    
    db.session.commit()
    
    return jsonify({"message": "Pins added to itinerary", "id": itinerary.id}), 200
    #TODO: Add functionality to delete pins from an itinerary
    
@views.route('/itinerary/<itinerary_id>', methods=['DELETE'])
def delete_itinerary(itinerary_id):
    """
    Delete an itinerary by its ID.
    Args:
        itinerary_id (int): The ID of the itinerary to be deleted.
    Returns:
        Response: A JSON response indicating the result of the deletion.
            - If the itinerary is not found or unauthorized, returns a 404 error with a message.
            - If the itinerary is successfully deleted, returns a 200 status with a success message.
    """
    itinerary = Itinerary.query.get(itinerary_id)
    
    if not itinerary:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    db.session.delete(itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary deleted"}), 200

@views.route('/itinerary/<itinerary_id>', methods=['PUT'])
def edit_itinerary(itinerary_id):
    """
    Edit the name of an existing itinerary.
    Args:
        itinerary_id (int): The ID of the itinerary to be edited.
    Returns:
        Response: A JSON response with a success message and the itinerary ID if the update is successful.
                  A JSON response with an error message and a 404 status code if the itinerary is not found or unauthorized.
    """
    itinerary = Itinerary.query.get(itinerary_id)
    if not itinerary:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    new_name = request.json.get('name')

    itinerary.name = new_name
    db.session.commit()
    
    return jsonify({"message": "Itinerary updated", "id": itinerary.id}), 200
    #known bug: if cancel is clicked on prompt, error message is displayed


@views.route('/places', methods=['GET','POST'])
def create_place():
    """
        Handle the creation and retrieval of places for the current user.
        GET:
        - Retrieve all places associated with the current user.
        - Returns a JSON list of places with their details.
        POST:
        - Create a new place with the provided details.
        - Requires 'name', 'longitude', and 'latitude' in the request JSON.
        - Optional fields: 'rating' and 'review'.
        - If a place with the same coordinates already exists for the user, returns an error message.
        - Otherwise, adds the new place to the database and returns a success message with the new place's ID.
        Returns:
        - On GET: JSON list of places.
        - On POST: JSON message indicating success or failure.
    """
    if request.method == 'GET':
        places = Place.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            "id": place.id,
            "name": place.name,
            "longitude": place.longitude,
            "latitude": place.latitude,
            "rating": place.rating,
            "review": place.review
        } for place in places])

    data = request.json
    name = data.get('name')
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    rating = data.get('rating')
    review = data.get('review')
    
    if not name or longitude is None or latitude is None:
        return jsonify({"error": "Pin name and coordinates are required"}), 400

    place_exists = db.session.query(Place).filter_by(user_id=current_user.id, longitude = longitude, latitude = latitude).first()

    new_place = Place(
            name=name,
            longitude=longitude,
            latitude=latitude,
            rating=rating,
            review=review,
            user_id=current_user.id,
    )
    if place_exists:
        return("Place already exists");
    else:
        db.session.add(new_place)
        db.session.commit()
        return jsonify({"message": "Place created", "id": new_place.id}), 201


@views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Delete a place from the database.
    Args:
        place_id (int): The ID of the place to be deleted.
    Returns:
        Response: A JSON response indicating the result of the deletion.
        - If the place is not found or unauthorized, returns a 404 error with an appropriate message.
        - If the place is successfully deleted, returns a 200 status with a success message.
    """
    place = Place.query.get(place_id)
    
    if not place:
        return jsonify({"error": "Itinerary not found or unauthorized"}), 404
    
    db.session.delete(place)
    db.session.commit()
    
    return jsonify({"message": "Place deleted"}), 200

@views.route('/places/<place_id>', methods=['PUT'])
def edit_place(place_id):
    """
    Edit the details of a place.
    Args:
        place_id (int): The ID of the place to be edited.
    Returns:
        Response: A JSON response containing a success message and the place ID if the update is successful.
                  A JSON response containing an error message if the place is not found or the user is unauthorized.
                  The response status code is 200 for success and 404 for errors.
    """
    place = Place.query.get(place_id)
    if not place or place.user_id != current_user.id:
        return jsonify({"error": "Place not found or unauthorized"}), 404

    new_name = request.json.get('name')
    if new_name:
        place.name = new_name
    
    new_rating = request.json.get('rating')
    new_review = request.json.get('review')
    
    if new_rating is not None:
        place.rating = new_rating
    if new_review is not None:
        place.review = new_review

    db.session.commit()
    return jsonify({"message": "Place updated", "id": place.id}), 200

@views.route('/user_places', methods=['GET'])
@login_required
def get_user_places():
    """
    Retrieve a list of places associated with the current user.

    This function queries the database for places that belong to the currently
    authenticated user and returns the data in JSON format.

    Returns:
        A JSON response containing a list of places, where each
        place is represented as a dictionary with the following keys:
            - id (int): The unique identifier of the place.
            - name (str): The name of the place.
            - longitude (float): The longitude coordinate of the place.
            - latitude (float): The latitude coordinate of the place.
            - rating (float): The rating of the place.
            - review (str): The review of the place.
    """
    places = Place.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "id": place.id,
        "name": place.name,
        "longitude": place.longitude,
        "latitude": place.latitude,
        "rating": place.rating,
        "review": place.review
    } for place in places])
