import requests


def get_token(name, expiry, strike):
    # Fetch the JSON data from the URL
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = requests.get(url)
    data = response.json()

    # Filter the data based on the given name, expiry, and strike
    for item in data:
        if (item['name'].upper() == name.upper() and
            item['expiry'] == expiry and
            float(item['strike']) == float(strike)):
            return item['token']
    return None


# Example usage
name = "NIFTY"
expiry = "18OCT2023"
strike = "20000"
token = get_token(name, expiry, strike)
if token:
    print(f"Token for {name} with expiry {expiry} and strike {strike} is: {token}")
else:
    print(f"No data found for {name} with expiry {expiry} and strike {strike}")
