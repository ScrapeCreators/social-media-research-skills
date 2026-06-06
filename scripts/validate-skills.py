#!/usr/bin/env python3
"""Lightweight validator for SKILL.md files in this repo."""
from pathlib import Path
import re
import sys

try:
    import yaml
except Exception as exc:
    print(f"Missing PyYAML: {exc}", file=sys.stderr)
    sys.exit(1)

root = Path(__file__).resolve().parents[1]
errors = []
for path in sorted(root.glob("skills/*/SKILL.md")):
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(root)
    if not text.startswith("---"):
        errors.append(f"{rel}: missing opening frontmatter fence")
        continue
    m = re.search(r"\n---\s*\n", text[3:])
    if not m:
        errors.append(f"{rel}: missing closing frontmatter fence")
        continue
    end = m.start() + 3
    raw = text[3:end]
    try:
        fm = yaml.safe_load(raw)
    except Exception as exc:
        errors.append(f"{rel}: invalid YAML: {exc}")
        continue
    if not isinstance(fm, dict):
        errors.append(f"{rel}: frontmatter is not a mapping")
        continue
    for key in ["name", "description"]:
        if not fm.get(key):
            errors.append(f"{rel}: missing {key}")
    if len(str(fm.get("description", ""))) > 1024:
        errors.append(f"{rel}: description is longer than 1024 chars")
    body = text[text.find("\n---", 3) + 5:].strip()
    if not body:
        errors.append(f"{rel}: empty body")

if errors:
    print("Skill validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"Validated {len(list(root.glob('skills/*/SKILL.md')))} skills")
