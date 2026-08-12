"""Safe fixture: credentials sourced from environment (paired with
vulnerable/config.py).

Expected: secrets-detection should NOT flag this file -- no credential
value is present in source, only references to environment variables. See
skills/secrets-detection/SKILL.md "False-Positive Conditions" -- environment
variable references.
"""

import os

# SAFE: no secret value in source -- read from environment/secret manager at runtime.
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

DATABASE_URL = os.environ["DATABASE_URL"]
