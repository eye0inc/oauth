from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os, time
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #to test with http://localhost
app = Flask(__name__)


# # github
# client_id = "0e76f7692426f08352c5"
# client_secret = "f0dc1020b31909ce186fe92f75d41f92119e716d"
# token_url = 'https://github.com/login/oauth/access_token'
# authorization_base_url = 'https://github.com/login/oauth/authorize'
# scope = []

# #o365 old
# client_id = "2e31a2e7-490d-4712-9a1b-dd6a7a478708"
# client_secret = "Q2YRN@2Q/us?hN]wMireQZn9k0AHn-Sw"
# token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
# authorization_base_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
# scope = ['openid', 'profile', 'email']

#o365 new
client_id = "20d83134-4aa9-46fd-86a2-c52108d6ef6c"
client_secret = "lAf7tSJRGs/40P9LzlSKcB[Ehamw:CW-"
token_url = "https://login.microsoftonline.com/9d4269c8-8d4d-4daa-a6f7-8144064472be/oauth2/v2.0/token"
authorization_base_url = "https://login.microsoftonline.com/9d4269c8-8d4d-4daa-a6f7-8144064472be/oauth2/v2.0/authorize"
scope = ['openid', 'profile', 'email']

@app.route("/")
def demo():
    if 'code' not in request.args:
        """Step 1: User Authorization:
        Redirect the user/resource owner to the OAuth provider (i.e. Github)
        using an URL with a few key OAuth parameters.
        """
        server = OAuth2Session(client_id, scope=scope)
        authorization_url, state = server.authorization_url(authorization_base_url)

        # State is used to prevent CSRF, keep this for later.
        session['oauth_state'] = state
        print ("DEMO", state, request.args)
        return redirect(authorization_url)


    # Step 2: User authorization, this happens on the provider.
    time.sleep(1)
    print ("CALLBACK", session['oauth_state'], request.args)
    print ("REQ.URL", request.url)
    i = request.url.find("?code=")+6
    tok = request.url[i:]
    print ("TOK:", tok)

    """ Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    server = OAuth2Session(client_id, state=session['oauth_state'])
    token = server.fetch_token(token_url, client_secret=client_secret,
                               # authorization_response=request.url)
                               authorization_response = "fougeddaboudit?code=%s" % tok)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    print ("PROFILE", request.args)
    """Fetching a protected resource using an OAuth 2 token.
    """
    server = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(server.get('https://api.github.com/user').json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True, port=7890, host="localhost")
