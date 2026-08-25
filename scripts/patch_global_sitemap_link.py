#!/usr/bin/env python3
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[1] / 'public'
MARK = 'data-site-directory-link'
BLOCK = '<div class="wrap" data-site-directory-link style="padding-top:14px;padding-bottom:14px;font-size:.86rem"><a href="/sitemap/">Sitemap / Site directory</a></div>'


def main():
    patched = 0
    already = 0
    for path in sorted(PUBLIC.rglob('*.html')):
        if path.name == '404.html':
            continue
        text = path.read_text(encoding='utf-8')
        if MARK in text:
            already += 1
            continue
        if '</footer>' not in text:
            continue
        path.write_text(text.replace('</footer>', BLOCK + '</footer>', 1), encoding='utf-8')
        patched += 1
    total = patched + already
    if total < 120:
        raise SystemExit(f'Expected sitemap footer link on >=120 pages, found {total}')
    print(f'Global HTML sitemap link OK: {total} pages expose /sitemap/ ({patched} patched, {already} already present)')


if __name__ == '__main__':
    main()
