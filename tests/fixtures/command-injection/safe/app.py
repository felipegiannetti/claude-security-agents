"""Safe fixture: argument-array execution, no shell (paired with
vulnerable/app.py).

Expected: injection-review should NOT confirm a command-injection finding
here -- `hostname` is passed as one element of an argument list to a
process-spawning call that never invokes a shell, so shell metacharacters
in it are inert. See
skills/injection-review/references/command-injection.md "False-Positive
Conditions".
"""

import re
import subprocess
from flask import Flask, request, abort

app = Flask(__name__)

HOSTNAME_PATTERN = re.compile(r"^[a-zA-Z0-9.-]+$")


@app.route("/diagnostics/ping")
def ping_host():
    hostname = request.args.get("host", "")
    if not HOSTNAME_PATTERN.match(hostname):
        abort(400)
    # SAFE: argument-array form, no shell=True -- shell metacharacters in
    # `hostname` are passed as a literal argument, never interpreted.
    output = subprocess.run(["ping", "-n", "1", hostname], shell=False, capture_output=True)
    return {"output": output.stdout.decode()}
