"""Safe fixture: algorithm pinned on JWT verification (paired with
vulnerable/app.py).

Expected: auth-authz-review should NOT confirm an authentication-bypass
finding here -- `algorithms=["RS256"]` pins the expected algorithm
server-side, so a token can't dictate its own verification method. See
skills/auth-authz-review/references/jwt.md "False-Positive Conditions".
"""

import jwt
from flask import Flask, request

app = Flask(__name__)

PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"


def decode_token(token):
    # SAFE: algorithm explicitly pinned -- the token's own header cannot
    # change which algorithm/key is used to verify it.
    return jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])


@app.route("/profile")
def profile():
    token = request.headers.get("Authorization", "").removeprefix("Bearer ")
    claims = decode_token(token)
    return {"user_id": claims["sub"]}
