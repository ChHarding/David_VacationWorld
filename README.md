# TripPin - HCI 5840 Project

## Description
TripPin is a web application that will allow you to map out places in the world that you have been to,
ability to plan for your next vacation with different itineraries, provide ratings and reviews to
different point-of-interests that users have visited. This app can also serve as a memory lane for users to remember their vacation.

## Installation and Run Locally

1. Clone the repository <br />
```git clone https://github.com/DavidTangJK/David_TripPin.git```

2. Enter directory <br />
```cd David_TripPin```

3. Install packages <br />
```pip install -r requirements.txt or pip3 install -r requirements.txt```

4. Get your own API Key <br />
To run this code locally, please procure your own api key from MapBox (https://account.mapbox.com/).
Once you got your apikey, create a .env file in the root folder and input this line of code: <br />```MAPBOX_API="your_api_key_in_between_the_quotes"```<br />
Save the .env file.

5. Run and see the website <br />
Run the main.py by selecting the Run Python File in Terminal play button in the top-right of the editor to start the server if you are using vscode.<br />
Navigate to http://127.0.0.1:5000 to see the site.

## How to use
### Login and Sign up
When you first get to the site, you will be prompted to login/sign up. Go over to "Sign Up" if this is your first time using. <img src="https://github.com/user-attachments/assets/c8e87e46-a8f7-4c71-a9e3-49bc42a480a2"/>
On the Sign Up screen, enter the required information. You may use fictitious emails and names. Note that the input fields have specific requirements. If your entries don't meet these criteria, you'll receive an error message. These are the requirements:
1. Email already exists in the database, please use a different email.
2. Email must be greater than 3 characters.
3. First name must be greater than 1 character.
4. Last name must be greater than 1 character.
5. Password must be at least 8 characters.
6. Passwords don\'t match.
<img src="https://github.com/user-attachments/assets/61b91d9f-3ecb-475d-bb72-1cb8e573a426" width=1200/>

Once you signed up/logged in, you should be greeted with the main page. This page will be where all functionality is located. There are some short instructions on the right to guide you through what you can do. 
<img src="https://github.com/user-attachments/assets/261de987-1865-42ce-b0c8-0b8b7ffcf581" />

### Add Pins 
One of the first things you can do on the main page is add a pin on the map. There are already 3 pins on the map automatically added for you to view and test, they cannot be deleted (unless there is a bug) but they can be edited. Press anywhere on the map and you would be prompted to add a pin on that specific spot. Enter the name, rating (1-5), and review for the pin, you may opt out from entering the rating and review.  
<img src="https://github.com/user-attachments/assets/ef07920f-873f-4d4e-b77f-93a7245719a8" width=400 height=350/>
<img src="https://github.com/user-attachments/assets/2482a351-9224-4622-a25b-a45ea8a2eb2c"/>
<img src="https://github.com/user-attachments/assets/34e1e2d5-d67e-4fbc-8f52-a033455da540"/>
<img src="https://github.com/user-attachments/assets/52fd5645-2fc9-46e4-87ca-bc179d1488c0"/>

You may also utilize the search bar and add a pin to the specific location. This provides more accuracy. After entering the location, the map will zoom in on the location and it will have a blue pin, this blue pin does not mean a pin is added onto the map. Click on the blue pin to insert a pin close to it, similar to how you add a pin before.  
<img src="https://github.com/user-attachments/assets/062d1af2-c04f-4928-b97a-0af32ce6a524"/>
<img src="https://github.com/user-attachments/assets/d3f4e15e-ad32-4689-9303-d23f56214f80"/>
<img src="https://github.com/user-attachments/assets/9adcc0b6-54c8-4c49-850a-2fb9e134af0b"/>


### © David Tang. All rights reserved.




