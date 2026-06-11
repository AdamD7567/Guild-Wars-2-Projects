import requests
import os

# Function that validates that the input is a valid ID (digit)
def validate_input(item):
    if not item.isdigit():
        print("Please enter a numeric item ID.")

    else:
        return True

# Function that takes a valid input and checks if the item exists.
# Returns the item information for the input ID or an appropriate status code and message if invalid.
def lookup_by_id(item_id):

    # Using requests.get to get the input item's information using ID
    response = requests.get(f"https://api.guildwars2.com/v2/items/{item_id}")
    data = response.json()

    # Print the item information if successfully found
    if response.status_code == 200:
        print("\nItem information\n--------------------")
        print("Name: ", data["name"])
        print("Type: ", data["type"])
        print("Rarity: ", data["rarity"])
        print("Level: ", data["level"])
        print("\nTrading Post Information\n--------------------")
        price_info = lookup_prices(item_id)
        if price_info is not None:
            print(price_info)

    # Returning appropriate error code and message if not found
    else:
        print("Error ", response.status_code, ": Could not find that item.", )
        print("API message:", data.get("text", "Unknown error"))

# Function that looks up the items buy and sell price on the Trading post.
# Takes in the item's ID and returns the current buying/selling information.
def lookup_prices(item_id):

    response = requests.get(f"https://api.guildwars2.com/v2/commerce/prices/{item_id}")
    data = response.json()
    
    if response.status_code == 200:
        buy_price = data["buys"]["unit_price"]
        sell_price = data["sells"]["unit_price"]
        spread_value = sell_price - buy_price
        return f"Buy price: {format_coins(buy_price)}\nSell price: {format_coins(sell_price)}\nSpread: {format_coins(spread_value)}"

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
    while searching:

        # Check input is valid first
        valid = False
        while not valid:
            input_item = input("Enter the ID of the item you are looking for: ")
            if validate_input(input_item) == True:
                valid = True
    
        # Lookup item
        lookup_by_id(input_item)

        search_check = input("\nPress x to quit, or any other key to continue: ")
        if (search_check == "x"):
            print("Thank you for using the lookup service! Goodbye!")
            searching = False

# Clearing the console on Entry TODO: Remove this when I move to frontend development.
clear = lambda: os.system('cls')
clear()
main()
