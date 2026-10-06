#!/usr/bin/env python3
"""Apply the shared localized contact labels after all page builders run."""

from __future__ import annotations

from pathlib import Path

import build_seo


def main() -> None:
    updated = 0
    for page in sorted(build_seo.PUBLIC.rglob("*.html")):
        original = page.read_text(encoding="utf-8")
        normalized = build_seo.label_footer_contacts(original)
        if normalized != original:
            page.write_text(normalized, encoding="utf-8")
            updated += 1

    print(f"Footer contact labels applied to {updated} HTML pages")


if __name__ == "__main__":
    main()
