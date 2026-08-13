"""Safe fixture: only non-sensitive fields logged (paired with
vulnerable/app.py).

Expected: logging-audit-review should NOT confirm a
sensitive-data-exposure-in-logs finding here -- the log call explicitly
allowlists the username and outcome, and never references the password
field or the raw request body. See
skills/logging-audit-review/references/sensitive-data-in-logs.md
"False-Positive Conditions".
"""

import logging

from flask import Flask, request

app = Flask(__name__)
logger = logging.getLogger(__name__)


def authenticate(username, password):
    stored_hash = lookup_password_hash(username)
    return stored_hash is not None and verify_hash(password, stored_hash)


@app.route("/login", methods=["POST"])
def handle_login():
    username = request.json.get("username")
    password = request.json.get("password")
    success = authenticate(username, password)

    # SAFE: explicit allowlist of non-sensitive fields -- the password
    # value and the raw request body are never passed to the logger.
    logger.info("login attempt", extra={"username": username, "success": success})

    if not success:
        return {"error": "invalid credentials"}, 401

    return {"status": "ok"}