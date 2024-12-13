# TripPin Developer Guide  

## Overview
TripPin is a web application that allows users to map out places they've visited, plan future vacations with itineraries, and provide ratings and reviews for different points of interest.  
It serves as a digital memory lane for users to remember their trips and share recommendations with others.  

## Current Implementation
The current version of TripPin implements the following features:
- User authentication (login/signup)
- Navigating map provided by Mapbox API
- Searching for locations using Mapbox API
- Adding, editing, and deleting pins on a map
- Leaving a rating and/or review for points of interest
- Creating and managing itineraries
- Associating pins with itineraries
- Viewing and interacting with pins and itineraries

## Installation and Deployment
Assuming the developer has followed the user guide for basic setup, here are additional steps for development:
1. Set up a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```
pip install -r requirements-dev.txt
```

3. Set up environment variables:
Create a .env file in the root directory with the following content:
```
MAPBOX_API="your_mapbox_api_key"
```

## User Interaction and Code Flow
### Program starts (__init__.py)
Once main.py is run, __init__.py will run through the function create_app and initialize the necessary information that the program requires, including app configurations and the database. Some key things to note is that ```app.permanent_session_lifetime = timedelta(days=5)``` stores the session for a maximum of 5 days, meaning if the user logs in on day 1, after day 5, the user will be logged out automatically. This is set up so that a user does not have to login every time they access the app.  

Another thing that is note-worthy is that all the other py files are imported in this file. If there is no existing database, __init__.py would also create one according to the context given and give a database name of "database.db". The database is using SQL, and the functions are all using SQLalchemy (more on that later in views.py)

The last thing that needs to be mentioned here about __init__.py is the usage of login_manager. login_manager is a package imported from flask_login to help with the initialization of the auth functions.

### User Authentication
#### base.html
As initialization is finished and the user accesses the website (assuming this is their first time or they are not logged in), they should be greeted by the login screen. There is a base.html that houses most of the styles of the login/signup pages, which are using Bootstrap styles. Another thing that is contained in the base.html is the template for the flash messages. These messages would be taken from auth.py. They could either be successful or failed messages such as 'Incorrect password, try again.' or 'Logged in successfully!'

#### login.html, sign_up.html, auth.py
When user auth.py handles login and signup logic.
3. User model in models.py is used to create and query user data.
4. Flask-Login manages user sessions.  


### Main Page Interaction
1. After authentication, user is directed to main_page.html.
2. Mapbox API is initialized with the user's API key.
3. views.py handles routes for fetching and manipulating data.  


### Adding Pins
1. The user clicks on the map or searches for a location.
2. addPin function in JavaScript sends a POST request to /places.
3. create_place function in views.py processes the request and creates a new Place object.
3. The pin is added to the map and the database.  


### Managing Itineraries
1. User creates an itinerary using the form in main_page.html.
2. create_itinerary function sends a POST request to /itinerary.
3. create_itinerary function in views.py creates a new Itinerary object.
4. Pins can be added to itineraries using the add_to_itinerary function.  


## Known Issues
### Minor Issues
1. Cancelling an itinerary edit shows an unnecessary error message.
2. Users cannot remove individual pins from an itinerary without deleting the entire itinerary.
3. Sometimes, pin details do not pull up and have to refresh the page. 

### Major Issues
There are no major breaking issues known at this time.

## Potential Improvements
1. Add ratings/reviews from Google Maps/Yelp so that users can see public ratings/reviews for that location.
2. Provide more description of the locations when searching.
3. Allow users to share pins/itineraries with others.
4. Ability to rate others pins
5. Allow users to see the top pins that others posted
6. Customizable UI/Map
7. Mobile friendly/accessible mobile app/webapp
