from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    address = db.Column(db.String(5000), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itinerary.id'), nullable=False)

class Itinerary(db.Model):
    __tablename__ = 'itinerary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    places = db.relationship('Place')

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    itineraries = db.relationship('Itinerary')