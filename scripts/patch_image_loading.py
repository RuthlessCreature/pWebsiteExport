#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
IMG_RE = re.compile(r'<img\b[^>]*\bsrc=["\'](/assets/photos/[^"\']+)["\'][^>]*>', re.I)
HERO_RE = re.compile(r'<section\b[^>]*class=["\'][^"\']*(?:photo-hero|page-hero|locale-hero)[^"\']*["\'][^>]*>.*?</section>', re.I | re.S)
ATTR_RE = {
    'loading': re.compile(r'\sloading=["\'][^"\']*["\']', re.I),
    'fetchpriority': re.compile(r'\sfetchpriority=["\'][^"\']*["\']', re.I),
    'decoding': re.compile(r'\sdecoding=["\'][^"\']*["\']', re.I),
}


def hero_ranges(text: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in HERO_RE.finditer(text)]


def in_ranges(pos: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= pos < end for start, end in ranges)


def normalize_tag(tag: str, hero: bool) -> str:
    for rx in ATTR_RE.values():
        tag = rx.sub('', tag)
    close = '/>' if tag.endswith('/>') else '>'
    body = tag[:-len(close)]
    attrs = ' loading="eager" fetchpriority="high" decoding="async"' if hero else ' loading="lazy" decoding="async"'
    return body + attrs + close


def patch(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding='utf-8')
    ranges = hero_ranges(text)
    hero_count = 0
    total = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal hero_count, total
        total += 1
        hero = in_ranges(match.start(), ranges)
        hero_count += int(hero)
        return normalize_tag(match.group(0), hero)

    patched = IMG_RE.sub(repl, text)
    if patched != text:
        path.write_text(patched, encoding='utf-8')
    return total, hero_count


def validate() -> tuple[int, int, int]:
    tags = 0
    high_pages = 0
    lazy_tags = 0
    failures: list[str] = []
    for path in sorted(PUBLIC.rglob('*.html')):
        text = path.read_text(encoding='utf-8')
        ranges = hero_ranges(text)
        local = list(IMG_RE.finditer(text))
        if not local:
            continue
        tags += len(local)
        high = 0
        hero_photos = 0
        for match in local:
            tag = match.group(0)
            hero = in_ranges(match.start(), ranges)
            hero_photos += int(hero)
            eager = 'loading="eager"' in tag
            lazy = 'loading="lazy"' in tag
            high_priority = 'fetchpriority="high"' in tag
            async_decode = 'decoding="async"' in tag
            if not async_decode:
                failures.append(f'{path}: missing decoding=async for {match.group(1)}')
            if hero:
                if not eager or not high_priority or lazy:
                    failures.append(f'{path}: hero photo is not eager/high: {match.group(1)}')
                high += int(high_priority)
            else:
                if not lazy or eager or high_priority:
                    failures.append(f'{path}: non-hero photo is not lazy/normal priority: {match.group(1)}')
                else:
                    lazy_tags += 1
        if high > 1:
            failures.append(f'{path}: {high} high-priority photos; expected at most one')
        if hero_photos > 1:
            failures.append(f'{path}: {hero_photos} local photos inside hero sections; expected at most one')
        if high == 1:
            high_pages += 1
    if tags < 400:
        failures.append(f'expected at least 400 local photo tags, found {tags}')
    if high_pages < 80:
        failures.append(f'expected at least 80 pages with a real hero photo, found {high_pages}')
    if failures:
        raise SystemExit('Image loading priority gate failed:\n' + '\n'.join(failures[:30]))
    return tags, high_pages, lazy_tags


def main() -> None:
    patched_tags = 0
    hero_tags = 0
    for path in sorted(PUBLIC.rglob('*.html')):
        total, hero = patch(path)
        patched_tags += total
        hero_tags += hero
    tags, high_pages, lazy_tags = validate()
    print(f'Image loading priority OK: {tags} local photos; {high_pages} hero/high-priority pages; {lazy_tags} lazy non-hero photos')


if __name__ == '__main__':
    main()
