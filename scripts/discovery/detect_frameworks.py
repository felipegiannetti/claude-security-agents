#!/usr/bin/env python3
"""Detect Frameworks

Heuristic framework detection from manifest files and dependency names -- a
starting hypothesis for agents/architecture-mapper.md, which should verify
against actual usage rather than trust this alone.

Usage:
    detect_frameworks.py --path <dir>
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

# manifest file -> (dependency-name-pattern -> (framework, kind))
NPM_SIGNATURES = {
    "react": ("React", "web"), "next": ("Next.js", "web"), "vue": ("Vue", "web"),
    "@angular/core": ("Angular", "web"), "express": ("Express", "web"),
    "@nestjs/core": ("NestJS", "web"), "fastify": ("Fastify", "web"),
    "prisma": ("Prisma", "orm"), "typeorm": ("TypeORM", "orm"), "sequelize": ("Sequelize", "orm"),
    "mongoose": ("Mongoose", "orm"), "apollo-server": ("Apollo GraphQL", "graphql"), "graphql": ("GraphQL", "graphql"),
    "handlebars": ("Handlebars", "template-engine"), "ejs": ("EJS", "template-engine"), "pug": ("Pug", "template-engine"),
}

PYTHON_SIGNATURES = {
    "django": ("Django", "web"), "flask": ("Flask", "web"), "fastapi": ("FastAPI", "web"),
    "sqlalchemy": ("SQLAlchemy", "orm"), "django-rest-framework": ("Django REST Framework", "web"),
    "graphene": ("Graphene GraphQL", "graphql"), "jinja2": ("Jinja2", "template-engine"),
    "grpcio": ("gRPC", "rpc"),
}

JAVA_SIGNATURES = {
    "spring-boot": ("Spring Boot", "web"), "spring-web": ("Spring Web", "web"),
    "hibernate": ("Hibernate", "orm"), "spring-data-jpa": ("Spring Data JPA", "orm"),
}


def detect_from_package_json(path: Path) -> list[dict]:
    findings = []
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return findings
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    for dep_pattern, (name, kind) in NPM_SIGNATURES.items():
        if any(dep_pattern in d for d in deps):
            findings.append({"name": name, "kind": kind, "evidence": [f"{path}: dependency matching '{dep_pattern}'"]})
    return findings


def detect_from_requirements(path: Path) -> list[dict]:
    findings = []
    try:
        text = path.read_text(encoding="utf-8-sig").lower()
    except OSError:
        return findings
    for dep_pattern, (name, kind) in PYTHON_SIGNATURES.items():
        if re.search(rf"^{re.escape(dep_pattern)}\b", text, re.MULTILINE):
            findings.append({"name": name, "kind": kind, "evidence": [f"{path}: matches '{dep_pattern}'"]})
    return findings


def detect_from_pom(path: Path) -> list[dict]:
    findings = []
    try:
        text = path.read_text(encoding="utf-8-sig").lower()
    except OSError:
        return findings
    for dep_pattern, (name, kind) in JAVA_SIGNATURES.items():
        if dep_pattern in text:
            findings.append({"name": name, "kind": kind, "evidence": [f"{path}: matches '{dep_pattern}'"]})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Directory to scan")
    args = parser.parse_args()

    root = Path(args.path)
    findings: list[dict] = []

    for pkg_json in root.rglob("package.json"):
        if "node_modules" in pkg_json.parts:
            continue
        findings.extend(detect_from_package_json(pkg_json))

    for req in list(root.rglob("requirements*.txt")) + list(root.rglob("pyproject.toml")):
        findings.extend(detect_from_requirements(req))

    for pom in root.rglob("pom.xml"):
        findings.extend(detect_from_pom(pom))

    # Deduplicate by name, merging evidence.
    by_name: dict[str, dict] = {}
    for f in findings:
        if f["name"] not in by_name:
            by_name[f["name"]] = f
        else:
            by_name[f["name"]]["evidence"].extend(f["evidence"])

    common.print_json({"frameworks": list(by_name.values())})
    return 0


if __name__ == "__main__":
    sys.exit(main())
