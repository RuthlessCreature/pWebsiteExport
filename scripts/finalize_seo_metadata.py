#!/usr/bin/env python3
"""Apply concise search titles and descriptive alt text to case archive images."""
from __future__ import annotations

import html
import re
from pathlib import Path

import build_seo as seo

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
    title = re.sub(r'\s*[—–-]\s*China Sourcing (?:Case|Scenario)\b', '', title, flags=re.I)
    if len(title) <= 70:
        return title

    # A colon often separates the main query from a long explanatory subtitle.
    brand = ' | Pomerol International' if re.search(r'\s\|\sPomerol International$', title, flags=re.I) else ''
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
    # Keep the shortened title semantically complete. A hard word-boundary cut
    # can leave a trailing preposition (for example, "... Checklist for | ...").
    dangling = {
        'a', 'an', 'the', 'for', 'of', 'to', 'in', 'on', 'with',
        'and', 'or', 'by', 'from', 'at', 'as', 'via',
    }
    while clipped and clipped.rsplit(' ', 1)[-1].casefold() in dangling:
        clipped = clipped.rsplit(' ', 1)[0].rstrip(' ,:;—–-')
    return clipped + suffix



def compact_description_metadata(text: str) -> str:
    primary = None
    for match in re.finditer(r'<meta\\b[^>]*>', text, flags=re.I):
        tag = match.group(0)
        name = re.search(r'\\bname=["\\\']([^"\\\']+)["\\\']', tag, flags=re.I)
        if name and name.group(1).casefold() == 'description':
            content = re.search(r'\\bcontent=["\\\'](.*?)["\\\']', tag, flags=re.I | re.S)
            if content:
                primary = seo.compact_description(html.unescape(content.group(1)))
                break
    if primary is None:
        return text

    def update_tag(match: re.Match[str]) -> str:
        tag = match.group(0)
        name = re.search(r'\\bname=["\\\']([^"\\\']+)["\\\']', tag, flags=re.I)
        prop = re.search(r'\\bproperty=["\\\']([^"\\\']+)["\\\']', tag, flags=re.I)
        key = (name.group(1) if name else prop.group(1) if prop else '').casefold()
        if key not in {'description', 'og:description', 'twitter:description'}:
            return tag
        content = re.search(r'\\bcontent=(["\\\'])(.*?)(\\1)', tag, flags=re.I | re.S)
        if not content:
            return tag
        quote = content.group(1)
        value = html.escape(primary, quote=True)
        return tag[:content.start()] + f'content={quote}{value}{quote}' + tag[content.end():]

    return re.sub(r'<meta\\b[^>]*>', update_tag, text, flags=re.I)

def main() -> None:
    changed_titles = 0
    changed_alts = 0
    for path in PUBLIC.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        text = compact_description_metadata(text)

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
