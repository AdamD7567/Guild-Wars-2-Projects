import requests
import os

# Function that validates that the input is a valid ID (digit)
def validate_input(item):
    if not item.isdigit():
        print("Please enter a numeric item ID.")

    else:
        return True

# Function that takes a valid input and checks if the item exists.
# Returns the item name for the ID or a status code if invalid.
def lookup_by_Id(input):

    # Using requests.get to get the input item's information using ID
    response = requests.get(f"https://api.guildwars2.com/v2/items/{input}")
    data = response.json()

    if response.status_code == 200:
        print(data["name"])
        price_info = lookup_prices(input)

        if price_info is not None:
            print(price_info)

    else:
        print("Error ", response.status_code, ": Could not find that item.", )
        print("API message:", data.get("text", "Unknown error"))

# Function that looks up the items buy and sell price on the Trading post
# Takes in the item's ID and returns the current buy and sell price
def lookup_prices(ID):

    response = requests.get(f"https://api.guildwars2.com/v2/commerce/prices/{ID}")
    data = response.json()
    
    if response.status_code == 200:
        buy_price = data["buys"]["unit_price"]
        sell_price = data["sells"]["unit_price"]
        return f"Buy price: {format_coins(buy_price)}\nSell price: {format_coins(sell_price)}"

    else:
        print(
            "Error ", 
            response.status_code, 
            ": Could not find Trading Post price.\nThis item may not be on the trading post."
            )

# Helper function that converts raw copper value into a readable format
# Takes in the copper value and returns the gold, silver, and copper value
def format_coins(copper):
    gold = copper // 10000
    silver = (copper % 10000) // 100
    copper = copper % 100

    return f"{gold}g {silver}s {copper}c"

# Program's entry point
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
