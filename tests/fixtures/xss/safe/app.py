"""Safe fixture: default auto-escaping (paired with vulnerable/app.py).

Expected: security-reviewer / security-verifier should NOT confirm an XSS
finding here -- templates/search.html has no `| safe` filter, so `query`
is rendered through Jinja2's default auto-escaping. See
skills/web-security-review/references/xss.md "False-Positive Conditions".
"""

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    return render_template("search.html", query=q)
