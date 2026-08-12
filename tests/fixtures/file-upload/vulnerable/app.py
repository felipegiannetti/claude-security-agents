"""Vulnerable fixture: Unrestricted File Upload (CWE-434).

Expected: file-security-review should flag `upload_avatar` -- the uploaded
file's extension/type is trusted from the client-supplied filename with no
content-based validation, and it's saved directly into a path served
statically by the web server, so an uploaded `.php`/`.py` file could be
requested and executed.
"""

import os
from flask import Flask, request

app = Flask(__name__)

STATIC_UPLOAD_DIR = "static/uploads"  # served directly by the web server


@app.route("/avatar", methods=["POST"])
def upload_avatar():
    file = request.files["avatar"]
    # VULNERABLE: filename (and therefore extension) is fully attacker-
    # controlled, and there is no content-based type check -- any file type
    # can be uploaded into a web-servable directory.
    save_path = os.path.join(STATIC_UPLOAD_DIR, file.filename)
    file.save(save_path)
    return {"url": f"/static/uploads/{file.filename}"}
