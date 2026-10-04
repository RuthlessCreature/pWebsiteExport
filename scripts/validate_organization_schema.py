#!/usr/bin/env python3
"""Keep the Organization identity in every JSON-LD graph aligned with build_seo.org()."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
sys.path.insert(0, str(ROOT / "scripts"))

import build_seo  # noqa: E402

JSONLD_RE = re.compile(
    r'<script\b[^>]*\btype=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
REQUIRED_KEYS = (
    "@id",
    "name",
    "legalName",
    "alternateName",
    "url",
    "logo",
    "email",
    "telephone",
    "address",
)


def main() -> None:
    expected = build_seo.org()
    organizations = 0
    errors: list[str] = []

    for page in sorted(PUBLIC.rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        for raw in JSONLD_RE.findall(html):
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{page}: malformed JSON-LD: {exc}")
                continue

            graph = data.get("@graph", [data]) if isinstance(data, dict) else data
            nodes = graph if isinstance(graph, list) else [graph]
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                node_type = node.get("@type", [])
                node_types = node_type if isinstance(node_type, list) else [node_type]
                if "Organization" not in node_types:
                    continue

                organizations += 1
                for key in REQUIRED_KEYS:
                    if node.get(key) != expected.get(key):
                        errors.append(f"{page}: Organization {key} differs from the shared definition")

    if not organizations:
        errors.append("no Organization nodes were found in public HTML")
    if errors:
        for error in errors[:30]:
            print(f"ERROR: {error}")
        raise SystemExit(f"Organization schema validation failed: {len(errors)} issue(s)")

    print(f"Organization schema OK: {organizations} nodes match the shared entity definition")


if __name__ == "__main__":
    main()
