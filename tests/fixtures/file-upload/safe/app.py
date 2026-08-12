"""Safe fixture: content-based validation + non-servable storage + generated
filename (paired with vulnerable/app.py).

Expected: file-security-review should NOT confirm a finding here -- the
file's actual content is verified as an image, the stored filename is
server-generated (never the client-supplied name), and storage is outside
any web-servable path. See
skills/file-security-review/references/file-upload.md and mime-validation.md
"False-Positive Conditions".
"""

import imghdr
import os
import uuid
from flask import Flask, request, abort

app = Flask(__name__)

PRIVATE_UPLOAD_DIR = "/var/app-storage/avatars"  # never served directly by the web server
ALLOWED_IMAGE_TYPES = {"jpeg", "png", "webp"}


@app.route("/avatar", methods=["POST"])
def upload_avatar():
    file = request.files["avatar"]
    content = file.read()

    # SAFE: content-based type check (magic bytes), not filename/Content-Type.
    detected_type = imghdr.what(None, h=content)
    if detected_type not in ALLOWED_IMAGE_TYPES:
        abort(400, "unsupported file type")

    # SAFE: server-generated filename -- client input never becomes a path segment.
    generated_name = f"{uuid.uuid4()}.{detected_type}"
    save_path = os.path.join(PRIVATE_UPLOAD_DIR, generated_name)
    with open(save_path, "wb") as f:
        f.write(content)

    return {"id": generated_name}
