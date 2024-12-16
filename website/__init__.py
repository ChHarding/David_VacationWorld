from flask import Flask, request, render_template, session, url_for, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta
from dotenv import load_dotenv

import os
load_dotenv()
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """
    Create and configure the Flask application.
    This function sets up the Flask application with necessary configurations,
    initializes the database, registers blueprints, and sets up the login manager.
    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.permanent_session_lifetime = timedelta(days=5)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
    app.config['SESSION_PERMANENT'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Itinerary, Place
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    """
    Creates a database if it does not already exist.

    Args:
        app: The Flask application database instance.

    Returns:
        None
    """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
