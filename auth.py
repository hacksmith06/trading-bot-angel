# Import necessary packages
from SmartApi import SmartConnect
import pyotp
import json

# Load configuration from config.json
with open('config.json', 'r') as file:
    config = json.load(file)

api_key = config["API_KEY"]
client_id = config["CLIENT_ID"]
password = config["PASSWORD"]
totp_token = config["TOTP_TOKEN"]

# Initialize the SmartConnect object
smart_api = SmartConnect(api_key)

# Generate TOTP for authentication
# get this from smart connect api website
totp = pyotp.TOTP(totp_token).now()

# Authenticate and establish a session
session_data = smart_api.generateSession(client_id, password, totp)
print(session_data)

# Extract authentication and refresh tokens
auth_token = session_data['data']['jwtToken']
refresh_token = session_data['data']['refreshToken']

# Fetch the feed token
feed_token = smart_api.getfeedToken()
print(feed_token)

# Fetch user profile
user_profile = smart_api.getProfile(refresh_token)
print(user_profile)

# Generate a new token using the refresh token
smart_api.generateToken(refresh_token)

# Extract and print available exchanges for the user
exchanges = user_profile['data']['exchanges']
print(exchanges)
