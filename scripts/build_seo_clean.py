#!/usr/bin/env python3
from __future__ import annotations

import build_seo

# Public source files are required to carry the production contact identity.
# Disable the legacy source-rewrite map so CI validates source truth instead of
# silently repairing stale contact data at build time.
build_seo.REPL = {}

if __name__ == '__main__':
    build_seo.main()
