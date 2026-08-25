#!/usr/bin/env python3
from pathlib import Path
import re

PUBLIC = Path(__file__).resolve().parents[1] / 'public'


def main():
    page = PUBLIC / 'sitemap' / 'index.html'
    if not page.is_file():
        raise SystemExit('missing public/sitemap/index.html')
    text = page.read_text(encoding='utf-8')
    links = re.findall(r'data-sitemap-link href="([^"]+)"', text)
    if len(links) < 120:
        raise SystemExit(f'expected >=120 sitemap links, found {len(links)}')
    if len(links) != len(set(links)):
        raise SystemExit('duplicate route in HTML sitemap')
    resources = (PUBLIC / 'resources' / 'index.html').read_text(encoding='utf-8')
    if 'href="/sitemap/"' not in resources or 'data-html-sitemap-link' not in resources:
        raise SystemExit('resources page does not expose HTML sitemap')
    xml = (PUBLIC / 'sitemap.xml').read_text(encoding='utf-8')
    if 'https://pomerol.in/sitemap/' not in xml:
        raise SystemExit('HTML sitemap missing from XML sitemap')
    print(f'HTML sitemap smoke OK: {len(links)} unique crawlable links')


if __name__ == '__main__':
    main()
