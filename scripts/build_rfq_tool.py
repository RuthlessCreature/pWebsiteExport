#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
URL = "https://pomerol.trade/tools/china-rfq-builder/"
TEMPLATE = ROOT / "scripts" / "templates" / "china-rfq-builder.html"


def add_tool_card(path: Path, heading: str) -> None:
    page = path.read_text(encoding="utf-8")
    if "data-rfq-tool-card" in page:
        return
    card = (
        '<section class="section" data-rfq-tool-card><div class="wrap"><article class="card">'
        '<div class="eyebrow">Free buyer tool</div>'
        f'<h2>{heading}</h2>'
        '<p>Turn product requirements into a structured China supplier RFQ and request comparable quote details. Your entries stay in your browser.</p>'
        '<a class="btn primary" href="/tools/china-rfq-builder/">Open the free RFQ builder →</a>'
        '</article></div></section>'
    )
    if "</main>" not in page:
        raise RuntimeError(f"Cannot find main content boundary in {path}")
    path.write_text(page.replace("</main>", card + "</main>", 1), encoding="utf-8")


def add_sitemap_entry() -> None:
    sitemap = PUBLIC / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    if URL in text:
        return
    entry = f"<url><loc>{URL}</loc></url>"
    if "</urlset>" not in text:
        raise RuntimeError("Cannot find sitemap urlset boundary")
    sitemap.write_text(text.replace("</urlset>", entry + "</urlset>", 1), encoding="utf-8")


def add_llms_entry() -> None:
    llms = PUBLIC / "llms.txt"
    text = llms.read_text(encoding="utf-8")
    if URL in text:
        return
    text += (
        "\n## Free buyer tool\n"
        f"- [China supplier RFQ builder]({URL}): Create a structured request for quotation and a comparable supplier response checklist. Inputs are processed in the browser and are not submitted or saved.\n"
    )
    llms.write_text(text, encoding="utf-8")


def main() -> None:
    target = PUBLIC / "tools" / "china-rfq-builder" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    for path, heading in (
        (PUBLIC / "resources" / "index.html", "Create a China supplier RFQ brief"),
        (PUBLIC / "resources" / "guides" / "index.html", "Use the free China supplier RFQ builder"),
    ):
        add_tool_card(path, heading)
    add_sitemap_entry()
    add_llms_entry()
    print("Free browser-only China supplier RFQ builder generated and linked")


if __name__ == "__main__":
    main()
