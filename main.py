import requests
from auth import authenticate
import json


# Read configuration from JSON file
with open("config-vidya.json", "r") as config_file:
    config = json.load(config_file)


# Function to fetch the token for a given option
def get_token_option(name, expiry, strike_and_option_type):
    # Fetch the JSON data from the URL and load it once
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = requests.get(url)
    data = response.json()

    # Construct the symbol based on the input
    symbol_pattern = f"{name}{expiry}{strike_and_option_type}"

    # Filter the loaded data based on the constructed symbol
    for item in data:
        if item.get('symbol') == symbol_pattern:
            return item.get('token'), item.get('symbol')
    return None, None


# Function to place an order
def place_order(name, expiry, strike_and_option_type):
    # Get authenticated smart_api and tokens from auth.py
    smart_api, auth_token, refresh_token, feed_token = authenticate()

    # Fetch the stock token using the get_token_option function
    token, symbol = get_token_option(name, expiry, strike_and_option_type)

    if token:
        try:
            orderparams = {
                "variety": "ROBO",
                "tradingsymbol": symbol,
                "symboltoken": token,
                "transactiontype": "BUY",
                "exchange": "NFO",
                "ordertype": "LIMIT",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": "53",
                "squareoff": "2",
                "stoploss": "1",
                "quantity": "15"
            }
            orderId = smart_api.placeOrder(orderparams)
            print("The order id is: {}".format(orderId))
        except Exception as e:
            print("Order placement failed: {}".format(e.message))
    else:
        print("Token not found for the given option.")


name = config["name"]
expiry = config["expiry"]
strike_and_option_type = config["strike_and_option_type"]

place_order(name, expiry, strike_and_option_type)
