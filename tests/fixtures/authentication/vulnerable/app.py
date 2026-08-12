"""Vulnerable fixture: JWT authentication bypass via algorithm confusion (CWE-347).

Expected: auth-authz-review should flag `decode_token` -- it decodes the
token without pinning the expected algorithm, so a token crafted with
`alg: none` (or swapped to HS256 using the RSA public key as an HMAC
secret) is accepted as valid.
"""

import jwt
from flask import Flask, request

app = Flask(__name__)

PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"


def decode_token(token):
    # VULNERABLE: no `algorithms=` allowlist -- the token's own header
    # dictates which algorithm/key is used to verify it.
    return jwt.decode(token, PUBLIC_KEY, options={"verify_signature": True})


@app.route("/profile")
def profile():
    token = request.headers.get("Authorization", "").removeprefix("Bearer ")
    claims = decode_token(token)
    return {"user_id": claims["sub"]}
