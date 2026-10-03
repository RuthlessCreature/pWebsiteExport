#!/usr/bin/env python3
from __future__ import annotations

import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urlsplit

HOST = "pomerol.trade"
BASE = f"https://{HOST}"
KEY = "6ef27e4a81efe1ff6c679ee852d012f2"
UA = "SEO-Monitor/2.0 (+https://pomerol.trade/)"


def fetch(url: str, user_agent: str = UA) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=25) as response:
        if response.status != 200:
            raise RuntimeError(f"{url}: HTTP {response.status}")
        return response.read().decode("utf-8", "replace")


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.titles: list[str] = []
        self.h1s: list[str] = []
        self.descriptions: list[str] = []
        self.robots: list[str] = []
        self.canonicals: list[str] = []
        self._title_open = False
        self._h1_depth = 0
        self._title_parts: list[str] = []
        self._h1_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self._title_open = True
            self._title_parts = []
            self.titles.append("")
        elif tag.lower() == "h1":
            self._h1_depth += 1
            if self._h1_depth == 1:
                self._h1_parts = []
                self.h1s.append("")
        elif tag.lower() == "meta":
            name = values.get("name", "").lower()
            if name == "description":
                self.descriptions.append(values.get("content", "").strip())
            elif name == "robots":
                self.robots.append(values.get("content", "").strip())
        elif tag.lower() == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonicals.append(values.get("href", "").strip())

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title" and self._title_open:
            self.titles[-1] = " ".join("".join(self._title_parts).split())
            self._title_open = False
        elif tag.lower() == "h1" and self._h1_depth:
            self._h1_depth -= 1
            if self._h1_depth == 0:
                self.h1s[-1] = " ".join("".join(self._h1_parts).split())

    def handle_data(self, data: str) -> None:
        if self._title_open:
            self._title_parts.append(data)
        if self._h1_depth:
            self._h1_parts.append(data)


def normalize_url(value: str) -> tuple[str, str, str, str, str]:
    parsed = urlsplit(value)
    path = parsed.path.rstrip("/") or "/"
    return parsed.scheme.lower(), parsed.hostname.lower() if parsed.hostname else "", str(parsed.port or ""), path, parsed.query


def inspect(url: str) -> tuple[str, MetadataParser, list[str]]:
    html = fetch(url)
    page = MetadataParser()
    page.feed(html)
    issues = []
    if len(page.titles) != 1 or not page.titles[0]:
        issues.append("title must appear exactly once and be non-empty")
    if len(page.h1s) != 1 or not page.h1s[0]:
        issues.append("H1 must appear exactly once and be non-empty")
    if len(page.descriptions) != 1 or not page.descriptions[0]:
        issues.append("meta description must appear exactly once and be non-empty")
    if len(page.canonicals) != 1 or not page.canonicals[0]:
        issues.append("canonical must appear exactly once and be non-empty")
    elif normalize_url(page.canonicals[0]) != normalize_url(url):
        issues.append("canonical does not match sitemap URL")
    if any(re.search(r"\bnoindex\b", item, re.IGNORECASE) for item in page.robots):
        issues.append("sitemap URL is marked noindex")
    return url, page, issues


robots = fetch(f"{BASE}/robots.txt")
llms = fetch(f"{BASE}/llms.txt")
contact = fetch(f"{BASE}/contact/")
key_file = fetch(f"{BASE}/{KEY}.txt").strip()
if key_file != KEY:
    raise RuntimeError("IndexNow key verification file does not match")
if not re.search(r"(?im)^sitemap:\s*https://pomerol\.trade/sitemap\.xml\s*$", robots):
    raise RuntimeError("robots.txt does not declare the production sitemap")
if not re.search(r"OAI-SearchBot|Claude-SearchBot|PerplexityBot", robots):
    raise RuntimeError("robots.txt does not include AI search crawlers")
if not re.search(r"(?ims)^User-agent:\s*Applebot\s*$[\s\S]*?^Allow:\s*/\s*$", robots):
    raise RuntimeError("robots.txt does not explicitly allow Applebot search")
if not re.search(r"(?ims)^User-agent:\s*Applebot-Extended\s*$[\s\S]*?^Disallow:\s*/\s*$", robots):
    raise RuntimeError("robots.txt does not explicitly block Applebot-Extended training")
if not llms.strip():
    raise RuntimeError("llms.txt is empty")
if "abd.yusuf.ibrahim.mustafa@gmail.com" not in contact or not re.search(r"132\D*4269\D*4270", contact) or "Yusuf" not in contact:
    raise RuntimeError("Contact page does not contain the unified contact details")

# Keep homepage and the focused sourcing-agent landing page aligned with their separate search intents.
for url, keyword in [
    (f"{BASE}/en/", "China product sourcing"),
    (f"{BASE}/china-sourcing-agent/", "China sourcing agent"),
]:
    _, page, issues = inspect(url)
    if issues:
        raise RuntimeError(f"{url}: {'; '.join(issues)}")
    if keyword.casefold() not in page.titles[0].casefold() or keyword.casefold() not in page.h1s[0].casefold():
        raise RuntimeError(f"{url}: title and H1 must cover {keyword!r}")

pending = deque([f"{BASE}/sitemap.xml"])
visited: set[str] = set()
urls: set[str] = set()
while pending:
    sitemap_url = pending.popleft()
    if sitemap_url in visited:
        continue
    visited.add(sitemap_url)
    root = ET.fromstring(fetch(sitemap_url))
    kind = root.tag.rsplit("}", 1)[-1]
    sitemap_ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    if kind == "sitemapindex":
        for node in root.findall(f"./{sitemap_ns}sitemap/{sitemap_ns}loc"):
            if node.text:
                pending.append(node.text.strip())
    elif kind == "urlset":
        for node in root.findall(f"./{sitemap_ns}url/{sitemap_ns}loc"):
            if node.text and node.text.strip().startswith(f"{BASE}/"):
                urls.add(node.text.strip())

if not urls:
    raise RuntimeError("Sitemap contains no canonical pomerol.trade URLs")
for url in urls:
    if urlsplit(url).hostname != HOST:
        raise RuntimeError(f"Non-canonical sitemap host: {url}")

failures: list[str] = []
titles: dict[str, list[str]] = {}
with ThreadPoolExecutor(max_workers=12) as executor:
    futures = [executor.submit(inspect, url) for url in sorted(urls)]
    for future in as_completed(futures):
        try:
            url, page, issues = future.result()
            if issues:
                failures.append(f"{url}: {'; '.join(issues)}")
            if page.titles and page.titles[0]:
                titles.setdefault(page.titles[0], []).append(url)
        except Exception as error:
            failures.append(str(error))
for title, matching_urls in titles.items():
    if len(matching_urls) > 1:
        failures.append(f"duplicate title {title!r}: {', '.join(sorted(matching_urls))}")
if failures:
    raise RuntimeError(f"Sitemap SEO checks failed ({len(failures)}):\n" + "\n".join(failures[:30]))

for bot in ("Googlebot", "bingbot", "OAI-SearchBot", "Claude-SearchBot", "PerplexityBot"):
    fetch(f"{BASE}/", bot)

print(f"{HOST}: robots, llms, {len(urls)} sitemap pages, unique titles, H1, descriptions, canonicals, indexability, contact, and search-intent checks passed")


