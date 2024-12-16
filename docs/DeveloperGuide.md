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
auth.py handles login and signup logic. When a user first gets to the login page, it has a route of /login, with a get and post method. The get method will render the login.html on the screen and prompt the user to log in. Once the user enters the data, the post method is triggered and sends the info to auth.py. auth.py will be connected to the database and check if the user information that is entered matches the data in the database with the code. ```User.query.filter_by(email=email).first()``` Messages will be flashed if there is an error/success during the login process.

This would be the same process and logic for the sign-up. The only caveat is that there are a couple of sign-up requirements, such as "Email must be greater than 3 characters", "First name must be greater than 1 character", "Password must be at least 8 characters," and so on. Once the user enters all the necessary information following the requirements, the info will be entered into the database, and the user will be redirected to the main page.

### Main function
#### main_page.html
The user will be greeted with the main_page after signing up/logging in. The map divs are taken from Mapbox examples code of displaying the map, make sure the styles and scripts are included from Mapbox. You will also see the Mapbox API key in the HTML, which is required to use the map assets provided by Mapbox. Half of the HTML contains code from the documentation for Mapbox, including map controls and settings, the search box to search for locations, pin information, the function for spinning the globe, and so on. The other half of the code contains functions dealing with pins (adding, editing, deleting), itineraries (creating, editing, deleting), and loading pins and itineraries onto the page according to the database. These functions will fetch user input/clicks and will be sent to views.py for further processing. After views.py processes, usually, it will send the results/error messages back to the client.

#### views.py
Views.py is where the magic happens. The main_page() function serves as the entry point, rendering the main page of the website with a Mapbox API key for map functionality. It requires user authentication to access.
The create_itinerary() function is an endpoint that handles both the creation and retrieval of user itineraries. When accessed via GET, it fetches all itineraries for the current user, including associated places. For POST requests, it creates a new itinerary, ensuring no duplicates exist for the user. The add_pins_to_itinerary() function allows users to add pins to specific itineraries, while delete_itinerary() and edit_itinerary() provide functionality to remove or modify existing itineraries.  

Pin management is handled by several functions. create_place() allows users to add new places or retrieve existing ones. It checks for duplicate places based on coordinates before adding new entries. The delete_place() and edit_place() functions provide options to remove or update place details, respectively. The pins contain the id, name, longitude, latitude, rating and review, and these pins are stored in the database. Lastly, the get_user_places() function retrieves all places associated with the current user, returning a comprehensive list of pin details and displaying it to the user. 

Throughout the code, proper error handling is implemented to manage scenarios such as missing data, unauthorized access, or non-existent records. The application utilizes Flask for routing and request handling, Flask-Login for user authentication, and SQLAlchemy ORM for database operations. This structure allows for a robust and maintainable web application focused on managing travel itineraries and places of interest.  

## Known Issues
### Minor Issues
1. Cancelling an itinerary edit shows an unnecessary error message.
2. Users cannot remove individual pins from an itinerary without deleting the entire itinerary.
3. Sometimes, pin details do not pull up, and you have to refresh the page. 

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
