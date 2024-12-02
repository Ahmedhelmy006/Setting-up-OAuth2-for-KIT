from flask import Flask, redirect, request, session, url_for
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)  
load_dotenv(dotenv_path='D:\Automated Data Pull\enviroment_variables.env')

client_id = os.getenv('KIT_OAUTH2_ID')
client_secret = os.getenv('KIT_OAUTH2_SECRET')

authorization_base_url = 'https://app.kit.com/oauth/authorize'
token_url = 'https://app.kit.com/oauth/token'

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

    # Check if the state parameter exists
    if not state:
        return "State mismatch error", 400

    # Create an OAuth2 session with the state
    kit = OAuth2Session(client_id, state=state, redirect_uri=url_for('kit_callback', _external=True))

    try:
        # Fetch the access token
        token = kit.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url
        )
    except Exception as e:
        return f"Error fetching token: {e}", 400

    # Save the token securely (e.g., in a database)
    # For demonstration, we'll store it in the session
    session['oauth_token'] = token

    # Redirect the user back to Kit using the redirect parameter
    kit_redirect = session.get('kit_redirect', 'https://app.kit.com/apps')
    return redirect(kit_redirect)

if __name__ == '__main__':
    # Run the app on port 5000
    app.run(host='0.0.0.0', port=5000)
