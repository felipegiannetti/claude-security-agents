"""Safe fixture: destination allowlist validated against the resolved IP
(paired with vulnerable/app.py).

Expected: web-security-review should NOT confirm an SSRF finding here --
the target host is resolved and checked against a private/internal IP
range before the request is made, and no redirect is followed past that
check. See skills/web-security-review/references/ssrf.md "False-Positive
Conditions".
"""

import ipaddress
import socket
from urllib.parse import urlparse

import requests
from flask import Flask, request, abort

app = Flask(__name__)

ALLOWED_HOSTS = {"images.trusted-cdn.example.com"}


def resolves_to_private_ip(hostname):
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return True  # fail closed: unresolvable host is treated as unsafe
    return any(ipaddress.ip_address(info[4][0]).is_private for info in addr_info)


@app.route("/link-preview")
def fetch_preview():
    url = request.args.get("url", "")
    parsed = urlparse(url)

    # SAFE: destination is checked against an explicit allowlist AND the
    # resolved IP is confirmed non-private before the request is made.
    if parsed.hostname not in ALLOWED_HOSTS or resolves_to_private_ip(parsed.hostname):
        abort(400, "destination not allowed")

    response = requests.get(url, timeout=5, allow_redirects=False)
    return {"status": response.status_code, "content_type": response.headers.get("Content-Type")}
