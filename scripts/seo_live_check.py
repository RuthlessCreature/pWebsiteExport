#!/usr/bin/env python3
from __future__ import annotations

import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque

HOST = "pomerol.trade"
BASE = f"https://{HOST}"
KEY = "6ef27e4a81efe1ff6c679ee852d012f2"
UA = "SEO-Monitor/1.0 (+https://pomerol.trade/)"


def fetch(url: str, user_agent: str = UA) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=25) as response:
        if response.status != 200:
            raise RuntimeError(f"{url}: HTTP {response.status}")
        return response.read().decode("utf-8", "replace")


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
if not llms.strip():
    raise RuntimeError("llms.txt is empty")
if "abd.yusuf.ibrahim.mustafa@gmail.com" not in contact or not re.search(r"132\D*4269\D*4270", contact) or "Yusuf" not in contact:
    raise RuntimeError("Contact page does not contain the unified contact details")

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
    if kind == "sitemapindex":
        for node in root.findall(".//{*}loc"):
            if node.text:
                pending.append(node.text.strip())
    elif kind == "urlset":
        for node in root.findall(".//{*}loc"):
            if node.text and node.text.strip().startswith(f"{BASE}/"):
                urls.add(node.text.strip())

if not urls:
    raise RuntimeError("Sitemap contains no canonical pomerol.trade URLs")
for bot in ("Googlebot", "bingbot", "OAI-SearchBot", "Claude-SearchBot", "PerplexityBot"):
    fetch(f"{BASE}/", bot)

print(f"{HOST}: robots, llms, {len(urls)} sitemap URLs, key, contact and 5 crawler requests passed")

