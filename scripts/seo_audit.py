#!/usr/bin/env python3
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
BASE = 'https://pomerol.in'

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.I | re.S)
DESC_RE = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', re.I)
CAN_RE = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', re.I)
H1_RE = re.compile(r'<h1\b', re.I)
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)
ALT_RE = re.compile(r'<link\s+rel=["\']alternate["\']\s+hreflang=["\']([^"\']+)["\']\s+href=["\']([^"\']+)["\']', re.I)
ROBOTS_RE = re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']', re.I)


def route_for_file(p: Path) -> str:
    rel = p.relative_to(PUBLIC).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-10]
    return '/' + rel


def file_for_route(route: str) -> Path | None:
    path = urlsplit(route).path
    if not path.startswith('/'):
        return None
    rel = path.lstrip('/')
    if not rel:
        return PUBLIC / 'index.html'
    direct = PUBLIC / rel
    if direct.is_file():
        return direct
    if path.endswith('/'):
        return PUBLIC / rel / 'index.html'
    candidate = PUBLIC / rel / 'index.html'
    if candidate.is_file():
        return candidate
    return direct


def local_url_to_file(url: str) -> Path | None:
    u = urlsplit(url)
    if u.scheme and u.netloc:
        if f'{u.scheme}://{u.netloc}' != BASE:
            return None
        return file_for_route(u.path)
    if url.startswith('/') and not url.startswith('//'):
        return file_for_route(url)
    return None


def main() -> None:
    html_files = sorted(PUBLIC.rglob('*.html'))
    errors: list[str] = []
    warnings: list[str] = []
    canon_by_file: dict[Path, str] = {}
    file_by_canon: dict[str, Path] = {}
    alternate_by_canon: dict[str, dict[str, str]] = {}
    title_count: Counter[str] = Counter()
    desc_count: Counter[str] = Counter()
    inbound: defaultdict[str, int] = defaultdict(int)

    for p in html_files:
        text = p.read_text(encoding='utf-8')
        route = route_for_file(p)
        robots = ROBOTS_RE.search(text)
        noindex = bool(robots and 'noindex' in robots.group(1).lower())
        if p.name == '404.html' or noindex:
            continue

        titles = TITLE_RE.findall(text)
        descs = DESC_RE.findall(text)
        cans = CAN_RE.findall(text)
        h1s = H1_RE.findall(text)
        if len(titles) != 1:
            errors.append(f'{route}: expected 1 title, found {len(titles)}')
        if len(descs) != 1:
            errors.append(f'{route}: expected 1 meta description, found {len(descs)}')
        if len(cans) != 1:
            errors.append(f'{route}: expected 1 canonical, found {len(cans)}')
            continue
        if len(h1s) != 1:
            errors.append(f'{route}: expected 1 H1, found {len(h1s)}')

        title = re.sub(r'\s+', ' ', titles[0]).strip() if titles else ''
        desc = re.sub(r'\s+', ' ', descs[0]).strip() if descs else ''
        can = cans[0]
        if title:
            title_count[title] += 1
        if desc:
            desc_count[desc] += 1
        if not can.startswith(BASE + '/'):
            errors.append(f'{route}: canonical outside production host: {can}')
        canon_by_file[p] = can
        if can in file_by_canon and route != '/':
            other = route_for_file(file_by_canon[can])
            if not ({route, other} == {'/', '/en/'}):
                warnings.append(f'duplicate canonical {can}: {other}, {route}')
        else:
            file_by_canon[can] = p

        expected = BASE + route
        if route != '/' and can != expected:
            errors.append(f'{route}: non-self canonical {can}, expected {expected}')
        if route == '/' and can != BASE + '/en/':
            errors.append(f'/: expected canonical {BASE}/en/, found {can}')

        alts = {lang: href for lang, href in ALT_RE.findall(text)}
        if alts:
            alternate_by_canon[can] = alts

        for href in HREF_RE.findall(text):
            target = local_url_to_file(href)
            if target is None:
                continue
            path = urlsplit(href).path
            if not target.exists():
                errors.append(f'{route}: broken internal link {path}')
                continue
            tt = target.read_text(encoding='utf-8') if target.suffix == '.html' else ''
            tc = CAN_RE.search(tt)
            if tc:
                inbound[tc.group(1)] += 1

    sitemap_path = PUBLIC / 'sitemap.xml'
    if not sitemap_path.is_file():
        errors.append('missing sitemap.xml')
        sitemap_urls: set[str] = set()
    else:
        root = ET.parse(sitemap_path).getroot()
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sitemap_urls = {n.text.strip() for n in root.findall('s:url/s:loc', ns) if n.text}

    canonical_urls = set(canon_by_file.values())
    for can in sorted(canonical_urls):
        if can not in sitemap_urls:
            errors.append(f'canonical missing from sitemap: {can}')
    for loc in sorted(sitemap_urls):
        if loc not in canonical_urls:
            errors.append(f'sitemap URL has no local canonical page: {loc}')

    for source_can, alts in alternate_by_canon.items():
        source_file = file_by_canon.get(source_can)
        if not source_file:
            continue
        for lang, target_url in alts.items():
            if lang == 'x-default':
                continue
            target_file = local_url_to_file(target_url)
            if target_file is None or not target_file.exists():
                errors.append(f'{source_can}: hreflang {lang} target missing: {target_url}')
                continue
            target_text = target_file.read_text(encoding='utf-8')
            target_can_match = CAN_RE.search(target_text)
            target_can = target_can_match.group(1) if target_can_match else target_url
            target_alts = {l: h for l, h in ALT_RE.findall(target_text)}
            if source_can not in target_alts.values():
                errors.append(f'{source_can}: hreflang target not reciprocal: {target_can}')

    for value, count in title_count.items():
        if count > 1:
            warnings.append(f'duplicate title x{count}: {value[:120]}')
    for value, count in desc_count.items():
        if count > 1:
            warnings.append(f'duplicate description x{count}: {value[:140]}')

    important_prefixes = (
        BASE + '/resources/guides/', BASE + '/zh/resources/guides/', BASE + '/ja/resources/guides/',
        BASE + '/ru/resources/guides/', BASE + '/es/resources/guides/', BASE + '/pt/resources/guides/',
        BASE + '/china-', BASE + '/industrial-', BASE + '/electronics-', BASE + '/automotive-',
        BASE + '/cnc-', BASE + '/solar-', BASE + '/hotel-', BASE + '/packaging-', BASE + '/warehouse-'
    )
    orphans = sorted(can for can in canonical_urls if can.startswith(important_prefixes) and inbound[can] == 0)
    if orphans:
        warnings.append(f'commercial/guide pages with zero static inbound links: {len(orphans)}')
        warnings.extend(f'orphan-warning: {x}' for x in orphans[:20])

    print(f'Technical SEO audit: {len(html_files)} HTML files, {len(canonical_urls)} canonical URLs, {len(sitemap_urls)} sitemap URLs, {len(alternate_by_canon)} hreflang-enabled canonicals')
    for w in warnings:
        print('SEO warning:', w)
    if errors:
        for e in errors:
            print('SEO ERROR:', e)
        raise SystemExit(f'Technical SEO audit failed with {len(errors)} error(s)')
    print(f'Technical SEO audit OK with {len(warnings)} warning(s)')


if __name__ == '__main__':
    main()
