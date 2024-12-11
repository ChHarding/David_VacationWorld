# TripPin Developer Guide  

## Overview
TripPin is a web application that allows users to map out places they've visited, plan future vacations with itineraries, and provide ratings and reviews for different points of interest.  
It serves as a digital memory lane for users to remember their trips and share recommendations with others.  

## Current Implementation
The current version of TripPin implements the following features:
- User authentication (login/signup)
- Searching for locations using Mapbox API
- Navigating map provided by Mapbox API
- Adding, editing, and deleting pins on a map
- Creating and managing itineraries
- Associating pins with itineraries
- Viewing user-specific pins and itineraries

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
### User Authentication
1. User navigates to /login or /sign-up routes.
2. auth.py handles login and signup logic.
3. User model in models.py is used to create and query user data.
4. Flask-Login manages user sessions.  


### Main Page Interaction
1. After authentication, user is directed to main_page.html.
2. Mapbox API is initialized with the user's API key.
3. views.py handles routes for fetching and manipulating data.  


### Adding Pins
1. User clicks on the map or searches for a location.
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

### Major Issues
There are no major breaking issues known at this time.

## Potential Improvements
1. Add ratings/reviews from Google Maps/Yelp so that users can see what the ratings/reviews for that location.
2. Provide more description to the locations when searching.
3. Allow users to share pins/itineraries with others.
4. Ability to rate others pins
5. Allow users to see top pins that others posted
6. Customizable UI/Map
7. Mobile friendly/accessible
