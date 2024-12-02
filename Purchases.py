from flask import Flask, redirect, request, session, url_for
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)

# Load secret key from environment or use a default for local testing
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

# Load environment variables
if os.getenv('RAILWAY_ENVIRONMENT') is None:  # Only load .env locally
    load_dotenv()

client_id = os.getenv('KIT_OAUTH2_ID')
client_secret = os.getenv('KIT_OAUTH2_SECRET')

authorization_base_url = 'https://app.kit.com/oauth/authorize'
token_url = 'https://app.kit.com/oauth/token'

@app.route('/')
def home():
    return "Welcome to the OAuth app! Use /kit/oauth to start the flow."

@app.route('/kit/oauth')
def kit_oauth():
    redirect_url = request.args.get('redirect')
    if redirect_url:
        session['kit_redirect'] = redirect_url
    else:
        session['kit_redirect'] = 'https://app.kit.com/apps'

    kit = OAuth2Session(client_id, redirect_uri=url_for('kit_callback', _external=True))
    authorization_url, state = kit.authorization_url(authorization_base_url)

    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route('/kit/oauth/callback')
def kit_callback():
    state = session.get('oauth_state')

    if not state:
        return "State mismatch error. Please start the authorization process again.", 400

    kit = OAuth2Session(client_id, state=state, redirect_uri=url_for('kit_callback', _external=True))

    try:
        token = kit.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url
        )
    except Exception as e:
        return f"Error fetching token: {e}. Ensure your client credentials and redirect URI are correct.", 400

    session['oauth_token'] = token
    kit_redirect = session.get('kit_redirect', 'https://app.kit.com/apps')
    return redirect(kit_redirect)

if __name__ == '__main__':
    app.run(debug=True)  # Only use this for local development
