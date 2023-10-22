# auth.py

# Import necessary packages
from SmartApi import SmartConnect
import pyotp
import json


def authenticate():
    # Load configuration from config.json
    with open('config-arpit.json', 'r') as file:
        config = json.load(file)

    api_key = config["API_KEY"]
    client_id = config["CLIENT_ID"]
    password = config["PASSWORD"]
    totp_token = config["TOTP_TOKEN"]

    # Initialize the SmartConnect object
    smart_api = SmartConnect(api_key)

    # Generate TOTP for authentication
    totp = pyotp.TOTP(totp_token).now()

    # Authenticate and establish a session
    session_data = smart_api.generateSession(client_id, password, totp)

    # Extract authentication and refresh tokens
    auth_token = session_data['data']['jwtToken']
    refresh_token = session_data['data']['refreshToken']

    # Fetch the feed token
    feed_token = smart_api.getfeedToken()

    # Generate a new token using the refresh token
    smart_api.generateToken(refresh_token)

    return smart_api, auth_token, refresh_token, feed_token


if __name__ == "__main__":
    smart_api, auth_token, refresh_token, feed_token = authenticate()
    print("Authentication Token:", auth_token)
    print("Refresh Token:", refresh_token)
    print("Feed Token:", feed_token)
