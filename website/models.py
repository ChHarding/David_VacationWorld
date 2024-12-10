from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Place(db.Model):
    """
    Represents a place in the database.

    Attributes:
        id (int): The unique identifier for the place.
        name (str): The name of the place.
        longitude (float): The longitude coordinate of the place.
        latitude (float): The latitude coordinate of the place.
        rating (int, optional): The rating of the place.
        review (str, optional): The review of the place.
        user_id (int): The ID of the user who added the place.
        itinerary_id (int, optional): The ID of the itinerary associated with the place.
    """
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(50000), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=True)

class Itinerary(db.Model):
    """
    Represents an itinerary in the database.

    Attributes:
        id (int): The primary key for the itinerary.
        name (str): The name of the itinerary, must be unique and not null.
        places (list): A list of places associated with the itinerary.
        user_id (int): The foreign key linking to the user who created the itinerary.
    """
    __tablename__ = 'itinerary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True, nullable=False)
    places = db.relationship('Place')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class User(db.Model, UserMixin):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user. Must be unique and not null.
        password (str): The hashed password of the user. Cannot be null.
        first_name (str): The first name of the user. Cannot be null.
        last_name (str): The last name of the user. Cannot be null.
        itineraries (list): A list of itineraries associated with the user.
        places (list): A list of places associated with the user.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    itineraries = db.relationship('Itinerary')
    places = db.relationship('Place')