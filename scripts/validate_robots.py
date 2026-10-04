#!/usr/bin/env python3
"""Fail a production build when Pomerol crawler access drifts from policy."""
from __future__ import annotations

import re
from pathlib import Path

robots_path = Path("public/robots.txt")
robots = robots_path.read_text(encoding="utf-8")

if not re.search(r"(?im)^Content-Signal:\s*search=yes,\s*ai-input=yes,\s*ai-train=no\s*$", robots):
    raise SystemExit(f"{robots_path}: must allow search and AI input while blocking AI training")

required_agents = (
    "Googlebot",
    "Bingbot",
    "YandexBot",
    "Baiduspider",
    "360Spider",
    "Sogou web spider",
    "Sogou inst spider",
    "OAI-SearchBot",
    "Claude-SearchBot",
    "PerplexityBot",
)
for agent in required_agents:
    if not re.search(rf"(?im)^User-agent:\s*{re.escape(agent)}\s*$", robots):
        raise SystemExit(f"{robots_path}: missing explicit search crawler rule for {agent}")

if not re.search(r"(?ims)^User-agent:\s*\*\s*$[\s\S]*?^Allow:\s*/\s*$", robots):
    raise SystemExit(f"{robots_path}: wildcard group must allow public pages")
if not re.search(r"(?ims)^User-agent:\s*\*\s*$[\s\S]*?^Disallow:\s*/api/\s*$", robots):
    raise SystemExit(f"{robots_path}: wildcard group must block API routes")
if not re.search(r"(?ims)^User-agent:\s*Applebot\s*$[\s\S]*?^Allow:\s*/\s*$", robots):
    raise SystemExit(f"{robots_path}: Applebot search must be allowed")
for agent in ("GPTBot", "ClaudeBot", "Applebot-Extended"):
    if not re.search(
        rf"(?ims)^User-agent:\s*{re.escape(agent)}\s*$[\s\S]*?^Disallow:\s*/\s*$",
        robots,
    ):
        raise SystemExit(f"{robots_path}: {agent} training access must be blocked")

if not re.search(r"(?im)^Sitemap:\s*https://pomerol\.trade/sitemap\.xml\s*$", robots):
    raise SystemExit(f"{robots_path}: missing canonical production sitemap")

print(f"{robots_path}: crawler allow/block rules and sitemap passed")
