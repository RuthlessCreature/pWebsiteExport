# HTML Sitemap build contract

The production build generates `/sitemap/` from current self-canonical HTML pages.

The generated directory must:

- expose at least 120 unique canonical targets;
- group core pages, sourcing services, case studies, English buyer guides, and five localized content families;
- be linked from `/resources/`;
- be included in `sitemap.xml`;
- pass the technical SEO auditor with no structural errors.

Do not hand-maintain the page list. Add or remove canonical pages through the normal site generators and let `scripts/build_html_sitemap.py` rebuild the directory.
