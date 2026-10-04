#!/usr/bin/env python3
from pathlib import Path
import json
import re

PUBLIC = Path(__file__).resolve().parents[1] / 'public'


def main():
    page = PUBLIC / 'sitemap' / 'index.html'
    if not page.is_file():
        raise SystemExit('missing public/sitemap/index.html')
    text = page.read_text(encoding='utf-8')
    match = re.search(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        raise SystemExit('HTML sitemap is missing JSON-LD')
    data = json.loads(match.group(1))
    graph = data.get('@graph', []) if isinstance(data, dict) else []
    organization = next((node for node in graph if node.get('@type') == 'Organization'), None)
    website = next((node for node in graph if node.get('@type') == 'WebSite'), None)
    if not organization or not website:
        raise SystemExit('HTML sitemap is missing Organization or WebSite entity')
    if website.get('publisher', {}).get('@id') != organization.get('@id'):
        raise SystemExit('HTML sitemap WebSite publisher does not reference Organization')
    if organization.get('email') != 'abd.yusuf.ibrahim.mustafa@gmail.com' or organization.get('telephone') != '+86 132 4269 4270':
        raise SystemExit('HTML sitemap Organization contact differs from shared identity')
    links = re.findall(r'data-sitemap-link href="([^"]+)"', text)
    if len(links) < 120:
        raise SystemExit(f'expected >=120 sitemap links, found {len(links)}')
    if len(links) != len(set(links)):
        raise SystemExit('duplicate route in HTML sitemap')
    resources = (PUBLIC / 'resources' / 'index.html').read_text(encoding='utf-8')
    if 'href="/sitemap/"' not in resources or 'data-html-sitemap-link' not in resources:
        raise SystemExit('resources page does not expose HTML sitemap')
    xml = (PUBLIC / 'sitemap.xml').read_text(encoding='utf-8')
    if 'https://pomerol.trade/sitemap/' not in xml:
        raise SystemExit('HTML sitemap missing from XML sitemap')
    print(f'HTML sitemap smoke OK: {len(links)} unique crawlable links')


if __name__ == '__main__':
    main()
