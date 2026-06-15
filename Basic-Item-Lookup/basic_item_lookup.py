import requests
import os

# Function that validates that the user's input is a valid ID (digit)
def validate_input(item):
    
    if not item.isdigit():
        print("Please enter a numeric item ID.")
        return False

    return True



# Function that takes in a valid item ID to display item information.
# Returns the item information for the input ID or an appropriate status code and message if it fails.
def lookup_by_id(item_id):

    data = make_api_request(f"https://api.guildwars2.com/v2/items/{item_id}")

    # Return nothing if no data is found
    if data is None:
        return

    # Print the item information if successfully found
    print("\nItem information\n--------------------")
    print("Name: ", data["name"])
    print("Type: ", data["type"])
    print("Rarity: ", data["rarity"])
    print("Level: ", data["level"])
    print("\nTrading Post Information\n--------------------")

    # Only displaying price information if the item is on the trading post
    price_info = lookup_prices(item_id)
    if price_info is not None:
        print(price_info)
    


# Function that looks up the items buy and sell price on the Trading post.
# Takes in the item's ID and returns the current buying/selling information.
def lookup_prices(item_id):

    data = make_api_request(f"https://api.guildwars2.com/v2/commerce/prices/{item_id}")

    # Returning None if no price data is found
    if data is None:
        return None
    
    buy_price = data["buys"]["unit_price"]
    sell_price = data["sells"]["unit_price"]
    spread_value = sell_price - buy_price
    
    return f"Buy price: {format_coins(buy_price)}\nSell price: {format_coins(sell_price)}\nSpread: {format_coins(spread_value)}"



# Helper function that converts raw copper value into a readable format
# Takes in the copper value and returns the gold, silver, and copper value
def format_coins(copper):
    gold = copper // 10000
    silver = (copper % 10000) // 100
    copper = copper % 100

    return f"{gold}g {silver}s {copper}c"



# Helper function used for making API requests and handling network errors/exceptions.
# Takes in the request url and returns either the response JSON file or the specific error that occured.
def make_api_request(url):

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Check if response is actually JSON before parsing
        if 'application/json' in response.headers.get('Content-Type', ''):
            return response.json()
        
        else:
            print("Error - response is not JSON.")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(f"Raw content: {response.text[:200]}")
            return None

    except requests.exceptions.ConnectionError:
        print("Connection failed - could not reach the server.")
        return None
    
    except requests.exceptions.Timeout:
        print("Request timed out - server took too long to respond.")
        return None

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code

        if status_code == 401:
            print("Unauthorised access - check your API key.")
        elif status_code == 404:
            print("Not found - check the URL or item ID.")
        elif status_code == 429:
            print("Rate limited - slow down your requests.")
        elif status_code >= 500:
            print(f"Server error {status_code} - try again later.")
        else:
            print(f"HTTP Error {status_code}: Something went wrong with the request.")

        return None

    except requests.exceptions.JSONDecodeError:
        print("Invalid JSON response!")
        return None
    
    # Catch all for other unspecified request-related errors
    except requests.exceptions.RequestException as e:
        print(f"Unexpected request error: {e}")
        return None


# TODO: Remove this when I move to frontend development.
# Helper function that clears the screen
def clear_console():
    os.system("cls")



# Program's entry point
def main():
    
    # Repeating loop
    searching = True
    while searching:

        # Check input is valid first
        valid = False
        while not valid:
            input_item = input("Enter the ID of the item you are looking for: ")
            if validate_input(input_item):
                valid = True
    
        # Lookup item
        lookup_by_id(input_item)

        search_check = input("\nPress x to quit, or any other key to continue: ")
        if search_check.lower() == "x":
            print("Thank you for using the lookup service! Goodbye!")
            searching = False

# Clearing the console on Entry 
if __name__ == "__main__":
    clear_console()
    main()
