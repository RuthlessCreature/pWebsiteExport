#!/usr/bin/env python3
from pathlib import Path
import add_image_dimensions
import build_guides_i18n as b
import build_html_sitemap
import build_localized_deep_pages
import enhance_hero_cases
import html_sitemap_smoke
import notify_indexnow
import patch_global_sitemap_link
import patch_image_loading
import patch_static_stylesheets
import seo_audit

b.PRIORITY = list(b.EN.keys())


def main():
    cases = b.load_cases()
    b.build_pages(cases)
    b.patch_english_hreflang()
    b.patch_local_homes()
    build_localized_deep_pages.main()
    enhance_hero_cases.main()
    build_html_sitemap.main()
    patch_global_sitemap_link.main()
    b.rebuild_sitemap()
    patch_static_stylesheets.main()
    patch_image_loading.main()
    add_image_dimensions.main()

    localized = []
    for code in b.LOCALES:
        root = b.PUBLIC / code / 'resources' / 'guides'
        localized.extend(root.glob('*/index.html'))
    assert len(localized) == 40, len(localized)

    for slug in b.PRIORITY:
        en = b.PUBLIC / 'resources' / 'guides' / slug / 'index.html'
        assert en.is_file(), en
        et = en.read_text(encoding='utf-8')
        for lang in ('zh-CN','ja','ru','es','pt','x-default'):
            assert f'hreflang="{lang}"' in et, (slug, lang)
        for code in b.LOCALES:
            p = b.PUBLIC / code / 'resources' / 'guides' / slug / 'index.html'
            assert p.is_file(), p
            t = p.read_text(encoding='utf-8')
            assert '"@type":"Article"' in t, p
            assert 'hreflang="en"' in t, p
            assert 'hreflang="x-default"' in t, p
            assert f'rel="canonical" href="https://pomerol.in/{code}/resources/guides/{slug}/"' in t, p

    for code in b.LOCALES:
        hub = b.PUBLIC / code / 'resources' / 'guides' / 'index.html'
        assert hub.is_file(), hub
        ht = hub.read_text(encoding='utf-8')
        for slug in b.PRIORITY:
            assert f'/{code}/resources/guides/{slug}/' in ht, (code, slug)

    sitemap = (b.PUBLIC / 'sitemap.xml').read_text(encoding='utf-8')
    for code in b.LOCALES:
        for slug in b.PRIORITY:
            assert f'https://pomerol.in/{code}/resources/guides/{slug}/' in sitemap, (code, slug)
    for code in b.LOCALES:
        for kind in ('services','about','resources','contact'):
            assert f'https://pomerol.in/{code}/{kind}/' in sitemap, (code, kind)
    assert 'https://pomerol.in/sitemap/' in sitemap

    html_sitemap = b.PUBLIC / 'sitemap' / 'index.html'
    assert html_sitemap.is_file(), html_sitemap
    st = html_sitemap.read_text(encoding='utf-8')
    assert st.count('data-sitemap-link') >= 140, st.count('data-sitemap-link')
    assert 'data-html-sitemap-link' in (b.PUBLIC / 'resources' / 'index.html').read_text(encoding='utf-8')

    footer_links = sum(1 for p in b.PUBLIC.rglob('*.html') if 'data-site-directory-link' in p.read_text(encoding='utf-8'))
    assert footer_links >= 140, footer_links

    localized_deep = sum(1 for code in b.LOCALES for kind in ('services','about','resources','contact') if (b.PUBLIC/code/kind/'index.html').is_file())
    assert localized_deep == 20, localized_deep

    hero_cases = sum(1 for p in (b.PUBLIC / 'case-studies').glob('*/index.html') if 'data-hero-control-plan' in p.read_text(encoding='utf-8'))
    assert hero_cases == 10, hero_cases

    key_file = b.PUBLIC / f'{notify_indexnow.KEY}.txt'
    assert key_file.is_file(), key_file
    assert key_file.read_text(encoding='utf-8').strip() == notify_indexnow.KEY

    print('Full multilingual guide SEO OK: 40 localized detail pages + 5 hubs + 8 reciprocal hreflang clusters')
    print(f'Localized deep SEO OK: {localized_deep} services/about/resources/contact pages + 4 six-language clusters')
    print(f'Hero case depth OK: {hero_cases} detailed sourcing control plans')
    print(f'Global sitemap footer discovery OK: {footer_links} HTML pages link to /sitemap/')
    print(f'Current IndexNow key source OK: {notify_indexnow.KEY}')
    html_sitemap_smoke.main()
    seo_audit.main()


if __name__ == '__main__':
    main()
