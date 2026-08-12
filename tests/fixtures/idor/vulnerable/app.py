"""Vulnerable fixture: Broken Object Level Authorization / IDOR (CWE-862).

Expected: security-reviewer should flag `get_invoice` -- it looks up an
invoice purely by the client-supplied `invoice_id`, with no check that the
authenticated caller actually owns (or is otherwise authorized to view)
that invoice. Any authenticated user can read any other user's invoice by
guessing/incrementing the ID.
"""

from flask import Flask, request, session

app = Flask(__name__)


def find_invoice_by_id(invoice_id):
    ...  # looks up and returns an Invoice regardless of owner


def require_login():
    if "user_id" not in session:
        raise PermissionError("not authenticated")
    return session["user_id"]


@app.route("/invoices/<int:invoice_id>")
def get_invoice(invoice_id):
    require_login()  # confirms the caller is authenticated...
    # VULNERABLE: ...but never checks that invoice.owner_id == current user.
    invoice = find_invoice_by_id(invoice_id)
    return {"invoice": invoice}
