"""Safe fixture: ownership check enforced (paired with vulnerable/app.py).

Expected: security-reviewer / security-verifier should NOT confirm a BOLA/
IDOR finding here -- `find_invoice_for_owner` scopes the lookup to the
authenticated caller, so an invoice_id belonging to another user simply
isn't found (404), not leaked. See
skills/api-security-review/references/bola-idor.md "False-Positive
Conditions".
"""

from flask import Flask, request, session, abort

app = Flask(__name__)


def find_invoice_for_owner(invoice_id, owner_id):
    ...  # looks up an Invoice ONLY if invoice.owner_id == owner_id, else None


def require_login():
    if "user_id" not in session:
        raise PermissionError("not authenticated")
    return session["user_id"]


@app.route("/invoices/<int:invoice_id>")
def get_invoice(invoice_id):
    current_user_id = require_login()
    # SAFE: lookup is scoped to the authenticated caller's own resources.
    invoice = find_invoice_for_owner(invoice_id, current_user_id)
    if invoice is None:
        abort(404)
    return {"invoice": invoice}
