from flask import Flask, render_template, request, redirect, url_for, flash
from SmartApi import SmartConnect
import pyotp
import json

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # for flash messages

# Load configuration from config.json
with open('config.json', 'r') as file:
    config = json.load(file)

api_key = config["API_KEY"]
client_id = config["CLIENT_ID"]
password = config["PASSWORD"]
totp_token = config["TOTP_TOKEN"]

smart_api = None
auth_token = None
refresh_token = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    global smart_api, auth_token, refresh_token

    smart_api = SmartConnect(api_key)
    totp = pyotp.TOTP(totp_token).now()
    session_data = smart_api.generateSession(client_id, password, totp)

    if 'data' in session_data:
        auth_token = session_data['data']['jwtToken']
        refresh_token = session_data['data']['refreshToken']
        flash('Authentication successful!', 'success')
    else:
        flash('Authentication failed!', 'danger')

    return redirect(url_for('index'))


@app.route('/fetch_historical_data', methods=['POST'])
def fetch_historical_data():
    exchange = request.form['exchange']
    symboltoken = request.form['symboltoken']
    interval = request.form['interval']
    fromdate = request.form['fromdate']
    todate = request.form['todate']

    historic_param = {
        "exchange": exchange,
        "symboltoken": symboltoken,
        "interval": interval,
        "fromdate": fromdate,
        "todate": todate
    }

    try:
        candle_data = smart_api.getCandleData(historic_param)
        return render_template('historical_data.html', candle_data=candle_data)
    except Exception as e:
        flash(f"Historic Api failed: {e.message}", 'danger')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
