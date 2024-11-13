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


messages = [{'title': 'Message One', 'content': 'Message One Content'},
            {'title': 'Message Two', 'content': 'Message Two Content'}]

itinerary = []

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    """user_id = db.Column(db.Integer, nullable=False)  # Assuming you have user authentication"""
    place = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name
        """self.user_id = user_id"""

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

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["email"]
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been logged out!, {user}")
    session.pop("user", None)
    return redirect(url_for("login"))
"""
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/add_location', methods=['POST'])
def add_location():
    location = request.form['location']
    if location:
        itinerary.append(location)
        flash('Location added to itinerary!')
    else:
        flash('Location cannot be empty!')
    return redirect(url_for('index'))
 """

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

def create_app():
    app = Flask(__name__)

    with app.app_context():
        db.create_all()

    return app

"""code to start server
from socket import gethostname
if 'liveweb' not in gethostname(): # all pythonanywhere servers have liveweb in their name"""
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8081)