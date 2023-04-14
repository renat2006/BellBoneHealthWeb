import json
import os
import time
from datetime import datetime, timedelta

import pytz as pytz
import requests
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from flask import url_for
from flask import current_app as app
import flask
from helpers import (
    session,
    redirect,
    Blueprint,
    request,
    updateSteps, getStepCounts
)

googleBlueprint = Blueprint("google", __name__)
load_dotenv()
# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v3/",
    client_kwargs={"scope": "openid email profile https://www.googleapis.com/auth/fitness.activity.read"},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)


@googleBlueprint.route('/g_login')
def g_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google.authorize', _external=True)
    session["origin"] = request.args.get('from')
    return google.authorize_redirect(redirect_uri)


@googleBlueprint.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    session["google_access_token"] = token['access_token']
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()

    session['google_info'] = user_info

    session.permanent = True
    if session["origin"] == 'signup':
        return redirect('/signup', code=307)
    elif session["origin"] == 'login':
        return redirect('/login/redirect=&', code=307)
