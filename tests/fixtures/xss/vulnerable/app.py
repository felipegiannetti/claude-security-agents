"""Vulnerable fixture: Reflected XSS (CWE-79).

Expected: security-reviewer should flag `search` -- the `q` query parameter
is rendered directly into the HTML response via a template string marked
safe/unescaped, rather than through Jinja2's default auto-escaping context.
"""

from flask import Flask, request, render_template_string

app = Flask(__name__)

# VULNERABLE: {{ query | safe }} disables Jinja2's default auto-escaping for
# this value, so attacker-controlled markup in `q` is rendered as-is.
TEMPLATE = """
<html><body>
  <p>You searched for: {{ query | safe }}</p>
</body></html>
"""


@app.route("/search")
def search():
    q = request.args.get("q", "")
    return render_template_string(TEMPLATE, query=q)
