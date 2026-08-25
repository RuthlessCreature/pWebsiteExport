#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
SITE_CSS = '<link rel="stylesheet" href="/assets/site.css">'
PHOTO_CSS = '<link rel="stylesheet" href="/assets/photo-cases.css">'
LOCALE_CSS = '<link rel="stylesheet" href="/assets/locale.css">'
PHOTO_MARKERS = (
    'photo-hero', 'photo-strip', 'photo-callout', 'case-preview',
    'case-library', 'case-study', 'case-index', 'case-filters',
)


def patch(path: Path) -> tuple[bool, bool]:
    text = path.read_text(encoding='utf-8')
    if SITE_CSS not in text:
        return False, False

    needs_locale = 'data-nav' in text
    needs_photo = any(marker in text for marker in PHOTO_MARKERS)
    additions: list[str] = []
    if needs_locale and LOCALE_CSS not in text:
        additions.append(LOCALE_CSS)
    if needs_photo and PHOTO_CSS not in text:
        additions.append(PHOTO_CSS)
    if not additions:
        return needs_locale, needs_photo

    text = text.replace(SITE_CSS, SITE_CSS + ''.join(additions), 1)
    path.write_text(text, encoding='utf-8')
    return needs_locale, needs_photo


def main() -> None:
    locale_pages = 0
    photo_pages = 0
    missing: list[str] = []
    for path in sorted(PUBLIC.rglob('*.html')):
        needs_locale, needs_photo = patch(path)
        if needs_locale:
            locale_pages += 1
        if needs_photo:
            photo_pages += 1

    for path in sorted(PUBLIC.rglob('*.html')):
        text = path.read_text(encoding='utf-8')
        if SITE_CSS not in text:
            continue
        if 'data-nav' in text and LOCALE_CSS not in text:
            missing.append(f'{path}: locale.css missing')
        if any(marker in text for marker in PHOTO_MARKERS) and PHOTO_CSS not in text:
            missing.append(f'{path}: photo-cases.css missing')

    site_js = (PUBLIC / 'assets' / 'site.js').read_text(encoding='utf-8')
    forbidden = ('document.createElement(\'link\')', 'document.createElement("link")', "'/assets/photo-cases.css'", "'/assets/locale.css'")
    if any(token in site_js for token in forbidden):
        missing.append('site.js still contains runtime stylesheet injection')

    if locale_pages < 100:
        missing.append(f'expected static locale.css on at least 100 nav pages, found {locale_pages}')
    if photo_pages < 50:
        missing.append(f'expected static photo-cases.css on at least 50 photo/case pages, found {photo_pages}')
    if missing:
        raise SystemExit('Static stylesheet gate failed:\n' + '\n'.join(missing[:30]))

    print(f'Static stylesheet discovery OK: locale.css on {locale_pages} pages; photo-cases.css on {photo_pages} pages; no runtime CSS injection')


if __name__ == '__main__':
    main()
