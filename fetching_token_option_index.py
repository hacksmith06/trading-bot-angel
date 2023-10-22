import requests

# Fetch the JSON data from the URL and load it once
url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = requests.get(url)
data = response.json()


def get_token(name, expiry, strike_and_option_type):
    # Construct the symbol based on the input
    symbol_pattern = f"{name}{expiry}{strike_and_option_type}"

    # Filter the loaded data based on the constructed symbol
    for item in data:
        if item.get('symbol') == symbol_pattern:
            return item.get('token')
    return None


name = "NIFTY"
expiry = "26OCT23"
strike_and_option_type = "20900PE"
token = get_token(name, expiry, strike_and_option_type)
if token:
    print(f"Token for {name} with expiry {expiry} and strike {strike_and_option_type} is: {token}")
else:
    print(f"No data found for {name} with expiry {expiry} and strike {strike_and_option_type}")
