import os
import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from flask import Flask, redirect, request, url_for
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
import webbrowser
import pyautogui


URL = "https://127.0.0.1:5000"

FB_CLIENT_ID = "1023286444899149"
FB_CLIENT_SECRET = "a51ee80147ee802c0c2c83c8c5b24534"

FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"

FB_SCOPE = ["email"]

GOOGLE_CLIENT_ID = '859640238570-mv9pkg6jknkta18e7s9rjvlr75rv52ln.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

CLIENT_ID = 'sso-app-zlhdcpobpg'
CLIENT_SECRET = 'zqontovlziypdjzjytgiuftloujlrkyhsnqnizqm'

AUTHORIZATION_BASE_URL = 'https://app.simplelogin.io/oauth2/authorize'
TOKEN_URL = 'https://app.simplelogin.io/oauth2/token'
USERINFO_URL = 'https://app.simplelogin.io/oauth2/userinfo'


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)



client = WebApplicationClient(GOOGLE_CLIENT_ID)


@app.route("/")
def index():
    if os.path.exists('profile_data.json'):
        return """
        <h2> You are already signed in </h2> <br>
        <a href = '/close'> Close </a> <br>
        <a href = '/sign_out'> Sign out </a>
        """
    else:
        return """
        <a href="/fb-login">Login with Facebook</a> <br>
        <a href = '/login_1'>Login with Simple Login</a> <br>
        <a class="button" href="/login">Login with Google</a> <br>
        <a href = '/close'> Close </a> <br>
        """


@app.route("/sign_out")
def sign_out():
    os.remove('profile_data.json')
    return f"""
    <h2> You are signed out! </h2> <br>
    <a href = '/'> Back </a>
    """

@app.route("/close")
def close():
    pyautogui.hotkey('ctrl', 'w')



@app.route("/fb-login")
def login_2():
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, redirect_uri=URL + "/fb-callback", scope=FB_SCOPE
    )
    authorization_url, _ = facebook.authorization_url(FB_AUTHORIZATION_BASE_URL)

    return redirect(authorization_url)


@app.route("/fb-callback")
def callback_2():
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, scope=FB_SCOPE, redirect_uri=URL + "/fb-callback"
    )

    # we need to apply a fix for Facebook here
    facebook = facebook_compliance_fix(facebook)

    facebook.fetch_token(
        FB_TOKEN_URL,
        client_secret=FB_CLIENT_SECRET,
        authorization_response=request.url,
    )

    # Fetch a protected resource, i.e. user profile, via Graph API

    facebook_user_data = facebook.get(
        "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
    ).json()

    email = facebook_user_data["email"]
    name = facebook_user_data["name"]
    picture_url = facebook_user_data.get("picture", {}).get("data", {}).get("url")


    output = {'name':name, 'email':email, 'picture':picture_url}

    with open('profile_data.json', 'w') as f:
        json.dump(output, f)

    return """<a href='/'> Back </a>"""

    #f"""
    #User information: <br>
    #Name: {name} <br>
    #Email: {email} <br>
    #Avatar <img src="{picture_url}"> <br>
    #<a href="/">Close</a>
    #"""

@app.route('/login_1')
def login_1():

    simplelogin = requests_oauthlib.OAuth2Session(
        CLIENT_ID, redirect_uri = 'https://localhost:5000/callback_1'
        )
    
    authorization_url, _ = simplelogin.authorization_url(AUTHORIZATION_BASE_URL)

    return redirect(authorization_url)


@app.route('/callback_1')
def callback_1():
    simplelogin = requests_oauthlib.OAuth2Session(CLIENT_ID)
    simplelogin.fetch_token(
        TOKEN_URL, client_secret = CLIENT_SECRET,
        authorization_response = request.url
        )

    user_info = simplelogin.get(USERINFO_URL).json()
    
    output = {'name':user_info["name"], 'email':user_info["email"], 'picture':user_info.get('avatar_url')}

    with open('profile_data.json', 'w') as f:
        json.dump(output, f)

    return """<a href='/'> Back </a>"""

    #f"""
    #User information: <br>
    #Name: {user_info["name"]} <br>
    #Email: {user_info["email"]} <br>
    #Avatar <img src = "{user_info.get('avatar_url')}"> <br>
    #<a href ="/">Close</a>
    #"""

@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    output = {'name':users_name, 'email':users_email, 'picture':picture}

    with open('profile_data.json', 'w') as f:
        json.dump(output, f)

    return  """<a href='/'> Back </a>"""

    # f"""
    #        User information: <br>
    #        Name: {users_name} <br>
    #        Email: {users_email} <br>
    #        Avatar <img src = "{picture}"> <br>
    #        <a href ="/">Close</a>
    #        """

def shutdown_server():
    func = request.environ.get('https://127.0.0.1:5000')
    if func is None:
        raise RuntimeError('Not running with the local server')
    func()    

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()   

if __name__ == "__main__":

    #webbrowser.open('https://127.0.0.1:5000')
    app.run(ssl_context = 'adhoc')