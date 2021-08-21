import os
from flask import g
from flask_oauthlib.client import OAuth

oauth = OAuth()

github = oauth.remote_app(
    "github",
    consumer_key=os.environ.get("GITHUB_CLIENT_ID"),
    consumer_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    request_token_params={"scope": "user:email"},
    base_url="https://api.github.com",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize"
)

@github.tokengetter
def get_github_token():
    if "access_token" in g:
        return g.access_token