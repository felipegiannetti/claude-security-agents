"""Vulnerable fixture: sensitive data logged in plaintext (CWE-532).

Expected: logging-audit-review should flag `handle_login` -- the entire
request body (including the plaintext password field) is logged on both
the failure and success paths, giving the log aggregation service its own
unprotected copy of user credentials. See
skills/logging-audit-review/references/sensitive-data-in-logs.md.
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
    # VULNERABLE: logs the entire request body, including the plaintext
    # "password" field, on every login attempt.
    logger.info("login attempt: %s", request.json)

    if not authenticate(request.json.get("username"), request.json.get("password")):
        return {"error": "invalid credentials"}, 401

    return {"status": "ok"}