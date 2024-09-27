import json
import os

# Data structure to store trips
trips = []
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "trips.json")

def add_trip():
    trip = {}
    trip['location'] = input("Enter the name of the location: ")
    trip['date'] = input("Enter the date (YYYY-MM-DD): ")
    trip['rating'] = input("Rate your trip (1-5): ")
    trip['review'] = input("Write a short review: ")
    trips.append(trip)
    print(f"Trip to {trip['location']} added successfully!\n")
    save_trips()

def show_trips():
    if not trips:
        print("No trips recorded yet.\n")
    else:
        for i, trip in enumerate(trips, 1):
            print(f"{i}. {trip['location']} on {trip['date']}")
            print(f"   Rating: {trip['rating']}")
            print(f"   Review: {trip['review']}\n")

def save_trips():
    with open(file_path, 'w') as file:
        json.dump(trips, file)
    print("Trips saved to 'trips.json' file.\n")

def load_trips():
    global trips
    try:
        with open(file_path, 'r') as file:
            trips = json.load(file)
        print("Trips loaded from 'trips.json'.\n")
    except FileNotFoundError:
        print("No saved trips found.\n")

def delete_trip():
    if not trips:
        print("No trips to delete.\n")
    else:
        show_trips()
        try:
            index = int(input("Enter the number of the trip you want to delete: ")) - 1
            if 0 <= index < len(trips):
                deleted_trip = trips.pop(index)
                print(f"Deleted trip to {deleted_trip['location']} on {deleted_trip['date']}.\n")
                save_trips()
            else:
                print("Invalid number. Please try again.\n")
        except ValueError:
            print("Please enter a valid number.\n")

def main():
    load_trips()
    while True:
        print("1. Add a new trip")
        print("2. Show all trips")
        print("3. Save trips")
        print("4. Delete trip")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_trip()
        elif choice == '2':
            show_trips()
        elif choice == '3':
            save_trips()
        elif choice == '4':
            delete_trip()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()