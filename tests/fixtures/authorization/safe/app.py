"""Safe fixture: role check enforced (paired with vulnerable/app.py).

Expected: api-security-review should NOT confirm a broken-function-level-
authorization finding here -- `require_admin` explicitly checks the
caller's role before the privileged action. See
skills/api-security-review/references/broken-function-authorization.md
"False-Positive Conditions".
"""

from flask import Flask, request, session, abort

app = Flask(__name__)


def require_admin():
    if "user_id" not in session:
        abort(401)
    if session.get("role") != "admin":
        abort(403)
    return session["user_id"]


def delete_user_by_id(user_id):
    ...  # deletes the user record


@app.route("/admin/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # SAFE: role is explicitly checked before the privileged action.
    require_admin()
    delete_user_by_id(user_id)
    return {"deleted": user_id}
