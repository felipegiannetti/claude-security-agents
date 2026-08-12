"""Vulnerable fixture: OS Command Injection (CWE-78).

Expected: injection-review should flag `ping_host` -- `hostname` is
attacker-controlled and concatenated directly into a shell command string
executed with `shell=True`, letting shell metacharacters (e.g. `; rm -rf`)
alter what actually runs.
"""

import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.route("/diagnostics/ping")
def ping_host():
    hostname = request.args.get("host", "")
    # VULNERABLE: shell=True + string concatenation lets shell metacharacters
    # in `hostname` inject additional commands.
    output = subprocess.run("ping -n 1 " + hostname, shell=True, capture_output=True)
    return {"output": output.stdout.decode()}
