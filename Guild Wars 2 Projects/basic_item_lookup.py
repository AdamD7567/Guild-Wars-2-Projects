import requests
import os

# Function that takes a valid input and checks if the item exists.
# Returns the item name for the ID or a status code if invalid.
def lookup_by_Id(input):

    # Using requests.get to get the input item's information using ID
    response = requests.get(f"https://api.guildwars2.com/v2/items/{input}")
    data = response.json()

    if response.status_code == 200:
        print(data["name"])

    else:
        print("Error ", response.status_code, ": Could not find that item.", )
        print("API message:", data.get("text", "Unknown error"))

# Function that validates that the input is a valid ID (digit)
def validate_input(item):
    if not item.isdigit():
        print("Please enter a numeric item ID.")

    else:
        return True

# Program entry point
def main():
    
    # Repeating loop
    searching = True
    while searching == True:

        # Check input is valid first
        valid = False
        while valid == False:
            item = input("Enter the ID of the item you are looking for: ")
            if validate_input(item) == True:
                valid = True
    
        # Lookup item
        lookup_by_Id(item)

        search_check = input("\nPress x to quit, or any other key to continue: ")
        if (search_check == "x"):
            print("Thank you for using the lookup service! Goodbye!")
            searching = False

# Clearing the console on Entry TODO: Remove this when I move to frontend development.
clear = lambda: os.system('cls')
clear()
main()
