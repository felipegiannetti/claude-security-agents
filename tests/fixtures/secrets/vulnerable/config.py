"""Vulnerable fixture: hardcoded cloud credential (CWE-798).

Expected: secrets-detection (via run_gitleaks.py) should flag the AWS access
key below. This key is a synthetic, non-functional value shaped to match
AWS's key format (AKIA + 16 chars) but is deliberately NOT the well-known
"AKIAIOSFODNN7EXAMPLE" documentation placeholder some scanners allowlist by
default -- using that literal value here would risk this fixture being
silently skipped instead of detected. This value grants no access to any
real account.
"""

# VULNERABLE: an AWS-shaped access key hardcoded directly in source.
AWS_ACCESS_KEY_ID = "AKIATESTFIXTURE12345"
AWS_SECRET_ACCESS_KEY = "tF1xtUr3S3cr3tK3yD0N0tUs3ThisVa1ueXX"

DATABASE_URL = "postgresql://admin:S3cr3tP4ss@prod-db.internal:5432/app"
