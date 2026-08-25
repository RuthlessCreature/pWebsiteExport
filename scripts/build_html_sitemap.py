#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
BASE = 'https://pomerol.in'
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.I | re.S)
CAN_RE = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', re.I)
ROBOTS_RE = re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']', re.I)

LOCALE_NAMES = {
    'zh': '中文',
    'ja': '日本語',
    'ru': 'Русский',
    'es': 'Español',
    'pt': 'Português',
}

GROUP_ORDER = [
    'Core company pages',
    'Sourcing services & industries',
    'Case studies',
    'English buyer guides',
    '中文',
    '日本語',
    'Русский',
    'Español',
    'Português',
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def route_for_file(path: Path) -> str:
    rel = path.relative_to(PUBLIC).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-10]
    return '/' + rel


def clean_title(text: str, route: str) -> str:
    match = TITLE_RE.search(text)
    if not match:
        return route
    return re.sub(r'\s+', ' ', html.unescape(match.group(1))).strip()


def classify(route: str) -> str:
    parts = [p for p in route.strip('/').split('/') if p]
    if parts and parts[0] in LOCALE_NAMES:
        return LOCALE_NAMES[parts[0]]
    if route.startswith('/case-studies/') or route == '/cases/':
        return 'Case studies'
    if route.startswith('/resources/guides/'):
        return 'English buyer guides'
    if route in {'/en/', '/services/', '/about/', '/contact/', '/resources/', '/privacy/', '/terms/'}:
        return 'Core company pages'
    return 'Sourcing services & industries'


def collect_pages() -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in sorted(PUBLIC.rglob('*.html')):
        if path.name == '404.html' or path.as_posix().endswith('/sitemap/index.html'):
            continue
        text = path.read_text(encoding='utf-8')
        robots = ROBOTS_RE.search(text)
        if robots and 'noindex' in robots.group(1).lower():
            continue
        canonical = CAN_RE.search(text)
        if not canonical:
            continue
        can = canonical.group(1)
        route = route_for_file(path)
        expected = BASE + route
        if route == '/' or can != expected:
            continue
        if can in seen:
            continue
        seen.add(can)
        pages.append({'route': route, 'canonical': can, 'title': clean_title(text, route), 'group': classify(route)})
    return pages


def patch_resources() -> None:
    path = PUBLIC / 'resources' / 'index.html'
    text = path.read_text(encoding='utf-8')
    if 'data-html-sitemap-link' in text:
        return
    block = ('<div class="resource" data-html-sitemap-link><div><strong>Full HTML site directory</strong>'
             '<span>Browse every indexable service page, case study and multilingual buyer guide from one crawlable directory.</span>'
             '</div><a class="small-link" href="/sitemap/">Open site directory →</a></div>')
    marker = '<div class="notice-box" style="margin-top:26px">'
    if marker not in text:
        raise RuntimeError('Resources page marker not found for HTML sitemap link')
    path.write_text(text.replace(marker, block + marker, 1), encoding='utf-8')


def render(pages: list[dict[str, str]]) -> str:
    groups: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for page in pages:
        groups[page['group']].append(page)
    for values in groups.values():
        values.sort(key=lambda item: (item['title'].lower(), item['route']))

    sections = []
    linked: set[str] = set()
    for group in GROUP_ORDER:
        values = groups.get(group, [])
        if not values:
            continue
        links = []
        for item in values:
            linked.add(item['canonical'])
            links.append(
                f'<li><a data-sitemap-link href="{esc(item["route"])}">{esc(item["title"])}</a>'
                f'<small>{esc(item["route"])}</small></li>'
            )
        sections.append(
            f'<section class="sitemap-group"><div class="sitemap-group-head"><h2>{esc(group)}</h2>'
            f'<span>{len(values)} pages</span></div><ul>{"".join(links)}</ul></section>'
        )

    expected = {page['canonical'] for page in pages}
    if linked != expected:
        missing = sorted(expected - linked)
        extra = sorted(linked - expected)
        raise RuntimeError(f'HTML sitemap coverage mismatch: missing={missing[:10]} extra={extra[:10]}')

    canonical = BASE + '/sitemap/'
    title = 'HTML Sitemap | Pomerol International'
    desc = 'Browse every indexable Pomerol International service page, sourcing case study and multilingual China sourcing buyer guide.'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow,max-snippet:-1"><link rel="icon" href="/assets/logo.svg"><link rel="stylesheet" href="/assets/site.css"><style>.sitemap-summary{{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}}.sitemap-summary span{{border:1px solid var(--line);border-radius:999px;padding:8px 12px;background:#fff;color:var(--muted)}}.sitemap-grid{{display:grid;gap:22px}}.sitemap-group{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px}}.sitemap-group-head{{display:flex;justify-content:space-between;gap:16px;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:8px}}.sitemap-group-head h2{{margin:0;font-size:1.3rem}}.sitemap-group-head span{{color:var(--muted);font-size:.9rem}}.sitemap-group ul{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 28px}}.sitemap-group li{{padding:10px 0;border-bottom:1px solid #edf0f2;display:flex;flex-direction:column;gap:3px}}.sitemap-group a{{font-weight:650}}.sitemap-group small{{color:var(--muted);overflow-wrap:anywhere}}@media(max-width:760px){{.sitemap-group ul{{grid-template-columns:1fr}}}}</style><script defer src="/assets/site.js"></script></head><body><header class="nav-shell"><nav class="nav wrap"><a class="brand" href="/en/"><img src="/assets/logo.svg" alt="Pomerol International"><span>Pomerol International<small>China sourcing & procurement</small></span></a><button class="menu-btn" data-menu aria-label="Menu">☰</button><div class="navlinks" data-nav><a href="/china-sourcing-agent/">Sourcing</a><a href="/services/">Services</a><a href="/cases/">Case Library</a><a href="/resources/guides/">Buyer Guides</a><a href="/resources/">Resources</a><a class="nav-cta" href="/contact/">Start an RFQ</a></div></nav></header><main><section class="page-hero"><div class="wrap"><div class="eyebrow">Crawlable site directory</div><h1 class="display">HTML Sitemap</h1><p>A complete human-readable directory of Pomerol International's indexable sourcing services, case studies and multilingual buyer guides.</p><div class="sitemap-summary"><span>{len(pages)} linked canonical pages</span><span>6 languages</span><span>Services · cases · buyer guides</span></div></div></section><section class="section"><div class="wrap sitemap-grid">{''.join(sections)}</div></section></main><footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="/en/"><img src="/assets/logo.svg" alt=""><span>Pomerol International<small>波美猴国际贸易（珠海）有限公司</small></span></a><p style="max-width:380px;color:#aebccd">China sourcing, procurement, OEM/ODM, quality control and export coordination for overseas buyers.</p></div><div><h4>Explore</h4><a href="/services/">Services</a><a href="/cases/">Case library</a><a href="/resources/guides/">Buyer guides</a></div><div><h4>Directory</h4><a href="/sitemap/">HTML sitemap</a><a href="/sitemap.xml">XML sitemap</a><a href="/resources/">Resources</a></div><div><h4>Yusuf</h4><a href="tel:+8613242694270">+86 132 4269 4270</a><a href="mailto:abd.yusuf.ibrahim.mustafa@gmail.com">abd.yusuf.ibrahim.mustafa@gmail.com</a><a href="https://wa.me/8613242694270">WhatsApp</a></div></div><div class="footer-bottom"><span>© 2026 Pomerol International Trade (Zhuhai) Co., Ltd.</span></div></div></footer></body></html>'''


def main() -> None:
    patch_resources()
    pages = collect_pages()
    if len(pages) < 120:
        raise SystemExit(f'Expected at least 120 canonical pages before HTML sitemap, found {len(pages)}')
    out = PUBLIC / 'sitemap'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(render(pages), encoding='utf-8')
    print(f'HTML sitemap OK: {len(pages)} canonical targets grouped into {len({p["group"] for p in pages})} sections')


if __name__ == '__main__':
    main()
