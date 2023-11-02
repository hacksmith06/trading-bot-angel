import requests
from auth import authenticate
import json
import time

# Read configuration from JSON file
with open("config-vidya.json", "r") as config_file:
    config = json.load(config_file)

# Authenticate once and get the smart_api object
smart_api, auth_token, refresh_token, feed_token = authenticate()


# Function to fetch the LTP data
def fetch_ltp_data(exchange, tradingsymbol, symboltoken):
    # Fetch the LTP data using the ltpData method
    ltp_response = smart_api.ltpData(exchange, tradingsymbol, symboltoken)
    return ltp_response


# Function to fetch the token for a given option
def get_token_option(name, expiry, strike_and_option_type):
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = requests.get(url)
    data = response.json()
    symbol_pattern = f"{name}{expiry}{strike_and_option_type}"
    for item in data:
        if item.get('symbol') == symbol_pattern:
            return item.get('token'), item.get('symbol')
    return None, None


# Function to monitor LTP and place order if condition is met
def monitor_and_place_order(smart_api, token, symbol, buy_price):
    while True:  # Infinite loop to keep checking the LTP
        ltp_data = fetch_ltp_data(smart_api, "NFO", symbol, token)
        ltp_value = ltp_data.get('data', {}).get('ltp', None)
        if ltp_value:
            print("LTP for the given option:", ltp_value)
            if buy_price - 1 <= ltp_value <= buy_price + 1:
                place_order(smart_api, token, symbol)  # Trigger the place order function
                break  # Exit the loop once order is placed
        else:
            print("LTP not found in the response.")
        time.sleep(1)  # Wait for 1 second before checking again


# Function to place an order
def place_order(smart_api, token, symbol):
    try:
        ltp_data = fetch_ltp_data(smart_api, "NFO", symbol, token)
        ltp = ltp_data.get('ltp', 0)
        orderparams = {
                "variety": "ROBO",
                "tradingsymbol": symbol,
                "symboltoken": token,
                "transactiontype": "BUY",
                "exchange": "NFO",
                "ordertype": "LIMIT",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": str(ltp),  # Use the fetched LTP as the price
                "squareoff": "2",
                "stoploss": "1",
                "quantity": "15"
            }
        orderId = smart_api.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(str(e)))


# Fetch the token once
name = config["name"]
expiry = config["expiry"]
strike_and_option_type = config["strike_and_option_type"]
token, symbol = get_token_option(name, expiry, strike_and_option_type)

if token:
    buy_price = float(config["buy_price"])
    monitor_and_place_order(smart_api, token, symbol, buy_price)
else:
    print("Token not found for the given option.")
