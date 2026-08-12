"""Vulnerable fixture: Server-Side Request Forgery (CWE-918).

Expected: web-security-review should flag `fetch_preview` -- the server
fetches whatever URL the client supplies with no destination restriction,
allowing a request to internal-only targets (e.g. a cloud metadata
endpoint or an internal admin service) using the server as a proxy.
"""

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route("/link-preview")
def fetch_preview():
    url = request.args.get("url", "")
    # VULNERABLE: no allowlist/host restriction -- `url` can point anywhere,
    # including internal-only hosts (e.g. http://169.254.169.254/...).
    response = requests.get(url, timeout=5)
    return {"status": response.status_code, "content_type": response.headers.get("Content-Type")}
