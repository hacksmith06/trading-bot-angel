# fetching_token_option_index.py

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
