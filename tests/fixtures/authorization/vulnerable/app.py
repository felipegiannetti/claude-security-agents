"""Vulnerable fixture: Broken Function-Level Authorization (CWE-862).

Expected: api-security-review should flag `delete_user` -- it checks that
the caller is authenticated, but never checks that the caller actually
holds the admin role before performing a privileged, irreversible action.
"""

from flask import Flask, request, session, abort

app = Flask(__name__)


def require_login():
    if "user_id" not in session:
        abort(401)
    return session["user_id"]


def delete_user_by_id(user_id):
    ...  # deletes the user record


@app.route("/admin/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    require_login()  # confirms the caller is authenticated...
    # VULNERABLE: ...but never checks session["role"] == "admin".
    delete_user_by_id(user_id)
    return {"deleted": user_id}
