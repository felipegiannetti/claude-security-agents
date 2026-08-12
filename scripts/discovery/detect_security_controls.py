#!/usr/bin/env python3
"""Detect Security Controls

Heuristic detection of existing security controls (authn/authz middleware,
validation libraries, CSRF protection, security headers, rate limiting) for
agents/architecture-mapper.md. This is context for the reviewer/verifier
("what protections already exist"), not evidence that everything is safe --
see agents/architecture-mapper.md "Existing Security Controls".

Usage:
    detect_security_controls.py --path <dir>
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

# dependency-name-substring -> control description
NPM_CONTROL_SIGNATURES = {
    "helmet": "Security headers middleware (helmet)",
    "csurf": "CSRF protection middleware (csurf)",
    "express-rate-limit": "Rate limiting middleware",
    "passport": "Authentication middleware (passport)",
    "joi": "Input validation library (joi)",
    "zod": "Input validation library (zod)",
    "express-validator": "Input validation middleware (express-validator)",
    "cors": "CORS middleware",
    "bcrypt": "Password hashing library (bcrypt)",
    "argon2": "Password hashing library (argon2)",
    "jsonwebtoken": "JWT library in use (verify configuration must still be checked)",
}

PYTHON_CONTROL_SIGNATURES = {
    "django-cors-headers": "CORS middleware",
    "djangorestframework-simplejwt": "JWT library in use (verify configuration must still be checked)",
    "flask-limiter": "Rate limiting middleware",
    "flask-talisman": "Security headers middleware",
    "passlib": "Password hashing library (passlib)",
    "bcrypt": "Password hashing library (bcrypt)",
    "pydantic": "Input validation library (pydantic)",
    "marshmallow": "Input validation library (marshmallow)",
}


def detect_from_package_json(path: Path) -> list[str]:
    controls = []
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return controls
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    for pattern, description in NPM_CONTROL_SIGNATURES.items():
        if any(pattern in d for d in deps):
            controls.append(description)
    return controls


def detect_from_requirements(path: Path) -> list[str]:
    controls = []
    try:
        text = path.read_text(encoding="utf-8-sig").lower()
    except OSError:
        return controls
    for pattern, description in PYTHON_CONTROL_SIGNATURES.items():
        if re.search(rf"^{re.escape(pattern)}\b", text, re.MULTILINE):
            controls.append(description)
    return controls


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Directory to scan")
    args = parser.parse_args()

    root = Path(args.path)
    controls: set[str] = set()

    for pkg_json in root.rglob("package.json"):
        if "node_modules" in pkg_json.parts:
            continue
        controls.update(detect_from_package_json(pkg_json))

    for req in list(root.rglob("requirements*.txt")) + list(root.rglob("pyproject.toml")):
        controls.update(detect_from_requirements(req))

    common.print_json({
        "existing_security_controls": [{"type": c, "location": "dependency manifest"} for c in sorted(controls)]
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())
