'''3. Implement OAuth2 authentication to allow users to log in using their Google or Facebook accounts.'''

from flask import Flask, redirect, url_for, session,request
from google.auth.transport import requests
from google.oauth2 import id_token

app = Flask(__name__)
#app.secret_key = 'your_secret_key'

CLIENT_ID = '528077041173-7qc1t0n20dl7ji7u7k3aodnipq4pa8ef.apps.googleusercontent.com'  # Replace with your Google Client ID


@app.route('/google-login')
def google_login():
    # Redirect users to Google's authorization URL
    auth_url = f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri=http://your_redirect_uri&scope=email profile openid'
    return redirect(auth_url)


@app.route('/google-auth')
def google_auth():
    # Handle the callback URL after Google login
    code = request.args.get('code')

    # Exchange code for tokens
    token_response = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': 'your_client_secret',  # Replace with your Google Client Secret
        'redirect_uri': 'http://your_redirect_uri',
        'grant_type': 'authorization_code'
    })

    # Get user information
    token_data = token_response.json()
    id_token_data = id_token.verify_oauth2_token(token_data['id_token'], requests.Request(), CLIENT_ID)

    # Access user data
    user_email = id_token_data.get('email')
    user_name = id_token_data.get('name')

    # Store user data in session or perform other actions
    session['user_email'] = user_email
    session['user_name'] = user_name

    return redirect(url_for('home'))


@app.route('/home')
def home():
    # Access user data from session after successful login
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    return f'Welcome, {user_name}! Your email is {user_email}' if user_email else 'Not logged in'


if __name__ == '__main__':
    app.run(debug=True)


import facebook
from flask import Flask, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'

APP_ID = '2072304809777419'  # Replace with your Facebook App ID
APP_SECRET = '84ffe89968c52b6ab6e74054df9d5ed5'  # Replace with your Facebook App Secret


@app.route('/facebook-login')
def facebook_login():
    # Redirect users to Facebook's authorization URL
    oauth_redirect_url = 'http://your_redirect_uri'
    login_url = f'https://www.facebook.com/v12.0/dialog/oauth?client_id={APP_ID}&redirect_uri={oauth_redirect_url}&scope=email'
    return redirect(login_url)


@app.route('/facebook-auth')
def facebook_auth():
    # Handle the callback URL after Facebook login
    oauth_redirect_url = 'http://your_redirect_uri'
    code = request.args.get('code')

    # Exchange code for access token
    graph = facebook.GraphAPI(version='v12.0')
    access_token = graph.get_access_token_from_code(
        code, oauth_redirect_url, APP_ID, APP_SECRET
    )

    # Get user information
    user_data = graph.get_object('me', fields='id,name,email')

    # Access user data
    user_email = user_data.get('email')
    user_name = user_data.get('name')

    # Store user data in session or perform other actions
    session['user_email'] = user_email
    session['user_name'] = user_name

    return redirect(url_for('home'))


@app.route('/home')
def home():
    # Access user data from session after successful login
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    return f'Welcome, {user_name}! Your email is {user_email}' if user_email else 'Not logged in'


if __name__ == '__main__':
    app.run(debug=True)
