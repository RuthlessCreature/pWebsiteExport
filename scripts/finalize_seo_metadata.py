#!/usr/bin/env python3
"""Apply concise search titles and descriptive alt text to case archive images."""
from __future__ import annotations

import html
import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[1] / 'public'
PHOTO_ALT = {
    'ev-charging.jpg': 'EV charging equipment sourcing case study',
    'industrial-vision.jpg': 'Industrial automation and machine vision sourcing case study',
    'glass-packaging.jpg': 'Glass packaging sourcing case study',
    'energy-storage.jpg': 'Energy storage equipment sourcing case study',
    'industrial-pumps.jpg': 'Industrial pump sourcing case study',
    'process-tanks.jpg': 'Process equipment sourcing case study',
    'warehouse-racking.jpg': 'Warehouse racking sourcing case study',
    'pendant-lighting.jpg': 'Hospitality lighting sourcing case study',
    'kitchen-cabinets.jpg': 'Kitchen cabinet sourcing case study',
    'hospitality-supplies.jpg': 'Hospitality supplies sourcing case study',
}


def concise_title(value: str) -> str:
    title = html.unescape(value).strip()
    title = re.sub(r'\s*[—–-]\s*China Sourcing Case', '', title, flags=re.I)
    title = re.sub(r'\s*\|\s*Pomerol International\s*$', ' | Pomerol', title, flags=re.I)
    if len(title) <= 70:
        return title

    # A colon often separates the main query from a long explanatory subtitle.
    brand = ' | Pomerol' if re.search(r'\s\|\sPomerol$', title, flags=re.I) else ''
    core = title[:-len(brand)] if brand else title
    if ':' in core:
        core = core.split(':', 1)[0].rstrip(' —–-')
        title = core + brand
    if len(title) <= 70:
        return title

    # Keep the original leading query phrase and brand while removing only the tail.
    suffix = brand
    limit = 70 - len(suffix)
    core = title[:-len(suffix)] if suffix else title
    clipped = core[:limit].rsplit(' ', 1)[0].rstrip(' ,:;—–-')
    return clipped + suffix


def main() -> None:
    changed_titles = 0
    changed_alts = 0
    for path in PUBLIC.rglob('*.html'):
        text = path.read_text(encoding='utf-8')

        def shorten(match: re.Match[str]) -> str:
            nonlocal changed_titles
            original = match.group(1)
            compact = concise_title(original)
            if compact != html.unescape(original).strip():
                changed_titles += 1
            return f'<title>{html.escape(compact)}</title>'

        text = re.sub(r'<title>(.*?)</title>', shorten, text, flags=re.I | re.S)

        def add_photo_alt(match: re.Match[str]) -> str:
            nonlocal changed_alts
            tag = match.group(0)
            src_match = re.search(r'\bsrc="([^"]+)"', tag, flags=re.I)
            if not src_match:
                return tag
            alt = PHOTO_ALT.get(src_match.group(1).rsplit('/', 1)[-1])
            if not alt:
                return tag
            existing = re.search(r'\balt\s*=\s*(["\'])(.*?)\1', tag, flags=re.I | re.S)
            if existing and existing.group(2).strip():
                return tag
            changed_alts += 1
            if existing:
                return tag[:existing.start()] + f'alt="{html.escape(alt, quote=True)}"' + tag[existing.end():]
            return tag[:-1] + f' alt="{html.escape(alt, quote=True)}">'

        # Only the static multilingual case hubs have photo images without alt;
        # preserve empty alt on the footer's redundant decorative logo.
        text = re.sub(r'<img\b[^>]*>', add_photo_alt, text, flags=re.I)
        path.write_text(text, encoding='utf-8')

    if changed_titles:
        print(f'Concise search titles applied: {changed_titles}')
    if changed_alts:
        print(f'Descriptive case-photo alt text added: {changed_alts}')


if __name__ == '__main__':
    main()
