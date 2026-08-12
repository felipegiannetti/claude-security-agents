"""Safe fixture: default auto-escaping (paired with vulnerable/app.py).

Expected: security-reviewer / security-verifier should NOT confirm an XSS
finding here -- `query` is rendered through Jinja2's default auto-escaping
(no `| safe` filter, no manual string interpolation into HTML), so markup in
`q` is rendered as inert text. See
skills/web-security-review/references/xss.md "False-Positive Conditions".
"""

from flask import Flask, request, render_template_string

app = Flask(__name__)

# SAFE: no `| safe` filter -- Jinja2 auto-escapes `query` by default.
TEMPLATE = """
<html><body>
  <p>You searched for: {{ query }}</p>
</body></html>
"""


@app.route("/search")
def search():
    q = request.args.get("q", "")
    return render_template_string(TEMPLATE, query=q)
