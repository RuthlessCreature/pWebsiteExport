#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
URL = "https://pomerol.trade/tools/china-rfq-builder/"
TEMPLATE = ROOT / "scripts" / "templates" / "china-rfq-builder.html"
sys.path.insert(0, str(ROOT / "scripts"))

import build_seo as seo  # noqa: E402

JSONLD_RE = re.compile(
    r'(<script\b[^>]*\btype=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.IGNORECASE | re.DOTALL,
)


def render_template() -> str:
    html = TEMPLATE.read_text(encoding="utf-8")
    match = JSONLD_RE.search(html)
    if not match:
        raise RuntimeError("RFQ builder template is missing its JSON-LD graph")
    graph = json.loads(match.group(2))
    nodes = graph.get("@graph")
    if not isinstance(nodes, list):
        raise RuntimeError("RFQ builder template JSON-LD is missing @graph")
    for node in nodes:
        if not isinstance(node, dict):
            continue
        if node.get("@type") == "Organization":
            node.clear()
            node.update(seo.org())
        elif node.get("@type") == "WebSite":
            node.clear()
            node.update(seo.website())
    encoded = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    return html[:match.start(2)] + encoded + html[match.end(2):]


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
    target.write_text(render_template(), encoding="utf-8")
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

