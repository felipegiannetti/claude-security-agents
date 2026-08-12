"""Vulnerable fixture: Reflected XSS (CWE-79).

Expected: security-reviewer should flag `search` -- the `q` query parameter
is rendered into templates/search.html via `{{ query | safe }}`, which
disables Jinja2's default auto-escaping for this value, so attacker-
controlled markup in `q` is rendered as-is.
"""

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    return render_template("search.html", query=q)
