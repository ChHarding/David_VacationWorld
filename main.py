
from dotenv import load_dotenv
from urllib.parse import urlencode
from flask import Flask, request, render_template
import os
load_dotenv()

app = Flask("Trip Pin")

@app.route("/")  
def main_page():
    html_str = render_template('index.html', title="Trip Pin") # title will be inlined in {{ title }}
    return html_str  # give it to the browser to display the inline page

@app.errorhandler(500)
def page_not_found(error):
    print(error) 
    s = "Error with " + str(request.args["URL"]) + "<br>" + str(error)   
    s = s + "<br>Hit the Back button and try something else ...)"
    return s

"""code to start server"""
from socket import gethostname
if 'liveweb' not in gethostname(): # all pythonanywhere servers have liveweb in their name
    app.run(debug=False, port=8081)

"""
# Data structure to store pins
pins = []
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "pins.json")

def add_pin():
    pin = {}
    pin['location'] = input("Enter the name of the location: ")
    pin['date'] = input("Enter the date (YYYY-MM-DD): ")
    pin['rating'] = input("Rate your pin (1-5): ")
    pin['review'] = input("Write a short review: ")
    pins.append(pin)
    print(f"pin to {pin['location']} added successfully!\n")
    save_pins()

def show_pins():
    if not pins:
        print("No pins recorded yet.\n")
    else:
        for i, pin in enumerate(pins, 1):
            print(f"{i}. {pin['location']} on {pin['date']}")
            print(f"   Rating: {pin['rating']}")
            print(f"   Review: {pin['review']}\n")

def save_pins():
    with open(file_path, 'w') as file:
        json.dump(pins, file)
    print("pins saved to 'pins.json' file.\n")

def load_pins():
    global pins
    try:
        with open(file_path, 'r') as file:
            pins = json.load(file)
        print("pins loaded from 'pins.json'.\n")
    except FileNotFoundError:
        print("No saved pins found.\n")

def delete_pin():
    if not pins:
        print("No pins to delete.\n")
    else:
        show_pins()
        try:
            index = int(input("Enter the number of the pin you want to delete: ")) - 1
            if 0 <= index < len(pins):
                deleted_pin = pins.pop(index)
                print(f"Deleted pin to {deleted_pin['location']} on {deleted_pin['date']}.\n")
                save_pins()
            else:
                print("Invalid number. Please try again.\n")
        except ValueError:
            print("Please enter a valid number.\n")

def main():
    load_pins()
    while True:
        print("1. Add a new pin")
        print("2. Show all pins")
        print("3. Save pins")
        print("4. Delete pin")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_pin()
        elif choice == '2':
            show_pins()
        elif choice == '3':
            save_pins()
        elif choice == '4':
            delete_pin()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
"""