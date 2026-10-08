#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
URL = "https://pomerol.trade/tools/china-supplier-verification-kit/"
TEMPLATE = ROOT / "scripts" / "templates" / "china-supplier-verification-kit.html"
sys.path.insert(0, str(ROOT / "scripts"))

import build_seo as seo  # noqa: E402


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def checklist_markup() -> str:
    path = PUBLIC / "resources" / "supplier-audit-checklist.csv"
    with path.open(encoding="utf-8-sig", newline="") as source:
        records = list(csv.DictReader(source))
    cards = []
    for index, record in enumerate(records, start=1):
        category = record["Section"].strip()
        item = record["Check item"].strip()
        evidence = record["Evidence requested"].strip()
        critical = record["Critical"].strip().lower() in {"yes", "true", "critical"}
        critical_attr = "true" if critical else "false"
        badge = '<span class="verification-critical-badge">Critical review item</span>' if critical else ""
        cards.append(
            f'<article class="verification-item" data-check-row data-category="{esc(category)}" '
            f'data-item="{esc(item)}" data-evidence="{esc(evidence)}" data-critical="{critical_attr}">'
            f'<div class="verification-category"><span>{esc(category)}</span>{badge}</div>'
            f'<h3>{esc(item)}</h3><p class="verification-evidence"><strong>Evidence to request:</strong> {esc(evidence)}</p>'
            f'<label for="review-status-{index}">Review status</label>'
            f'<select id="review-status-{index}" data-status>'
            '<option value="not-reviewed">Not reviewed</option>'
            '<option value="evidence-recorded">Evidence recorded</option>'
            '<option value="follow-up">Follow-up required</option>'
            '<option value="concern">Unresolved concern</option>'
            '</select>'
            f'<label for="review-note-{index}">Private note (optional)</label>'
            f'<textarea id="review-note-{index}" placeholder="Record the document, date, question or owner to follow up."></textarea>'
            '</article>'
        )
    return "\n".join(cards)


def tool_card(heading: str) -> str:
    return (
        '<section class="section" data-supplier-verification-kit-card><div class="wrap">'
        '<article class="card"><div class="eyebrow">Free buyer tool · China supplier verification</div>'
        f'<h2>{esc(heading)}</h2>'
        '<p>Track supplier identity, production scope, quality evidence, documents and payment controls. '
        'Selections stay in the browser and the review is not a certification or pass/fail result.</p>'
        f'<a class="btn primary" href="{URL}">Open the free supplier verification tracker →</a>'
        '</article></div></section>'
    )


def add_card(relative_path: str, heading: str) -> None:
    path = PUBLIC / relative_path
    text = path.read_text(encoding="utf-8")
    if "data-supplier-verification-kit-card" in text:
        return
    if "</main>" not in text:
        raise RuntimeError(f"Cannot find main content boundary in {path}")
    path.write_text(text.replace("</main>", tool_card(heading) + "</main>", 1), encoding="utf-8")


def add_sitemap_entry() -> None:
    path = PUBLIC / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    if URL in text:
        return
    if "</urlset>" not in text:
        raise RuntimeError("Cannot find sitemap urlset boundary")
    path.write_text(text.replace("</urlset>", f"<url><loc>{URL}</loc></url></urlset>", 1), encoding="utf-8")


def add_llms_entry() -> None:
    path = PUBLIC / "llms.txt"
    text = path.read_text(encoding="utf-8")
    if URL in text:
        return
    text += (
        "\n## Free buyer tool\n"
        f"- [China supplier verification checklist and evidence tracker]({URL}): Review legal identity, "
        "factory role, production scope, quality controls, documents and payment evidence; export a review CSV locally. "
        "The tool does not verify, certify or approve a supplier.\n"
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    title = "China Supplier Verification Checklist & Evidence Tracker | Pomerol"
    description = (
        "Use a free China supplier verification checklist to track legal identity, factory role, "
        "production capability, quality controls, documents and payment evidence."
    )
    template = TEMPLATE.read_text(encoding="utf-8")
    tags = seo.seo_tags(
        title,
        description,
        URL,
        "en",
        f"{seo.BASE}/assets/photos/product-development.jpg",
        extra=[seo.crumbs(URL, "China Supplier Verification Checklist")],
    )
    rendered = template.replace("{{SEO_TAGS}}", tags).replace("{{CHECKLIST_ROWS}}", checklist_markup())
    target = PUBLIC / "tools" / "china-supplier-verification-kit" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")

    for relative_path, heading in (
        ("resources/index.html", "Use an evidence tracker before committing to a supplier"),
        ("resources/guides/index.html", "Turn the supplier verification guide into a working review"),
        (
            "resources/guides/china-supplier-verification-checklist/index.html",
            "Track supplier evidence with the free verification checklist",
        ),
        ("china-sourcing-agent/index.html", "Track evidence before comparing sourcing candidates"),
        ("china-quality-inspection/index.html", "Connect supplier evidence to quality checkpoints"),
    ):
        add_card(relative_path, heading)
    add_sitemap_entry()
    add_llms_entry()
    print("Supplier verification evidence tracker generated and linked")


if __name__ == "__main__":
    main()
