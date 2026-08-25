#!/usr/bin/env python3
import json
from pathlib import Path

import build_seo as seo

ROOT = Path(__file__).resolve().parents[1]
DETAILS = json.loads((ROOT / 'scripts' / 'hero_case_details.json').read_text(encoding='utf-8'))


def bullets(items):
    return ''.join(f'<li>{seo.esc(x)}</li>' for x in items)


def section(detail):
    return (
        '<section class="section" data-hero-control-plan>'
        '<div class="wrap">'
        '<div class="section-head"><div><div class="eyebrow">Detailed sourcing control plan</div>'
        '<h2 class="display">From requirement freeze to shipment handover.</h2></div>'
        '<p>This expanded control plan is a representative procurement method for this product category. '
        'It does not claim that every listed step was performed for a named client or shipment.</p></div>'
        '<div class="grid-2">'
        f'<article class="card"><h3>1. Requirement snapshot</h3><ul>{bullets(detail["requirements"])}</ul></article>'
        f'<article class="card"><h3>2. Supplier screening</h3><ul>{bullets(detail["screening"])}</ul></article>'
        f'<article class="card"><h3>3. Validation gates</h3><ul>{bullets(detail["validation"])}</ul></article>'
        f'<article class="card"><h3>4. Buyer handover pack</h3><ul>{bullets(detail["handover"])}</ul></article>'
        '</div>'
        '<div class="notice-box" style="margin-top:26px"><strong>Use the same controls on your project:</strong> '
        '<a href="/resources/supplier-audit-checklist.csv">Supplier audit checklist</a> · '
        '<a href="/resources/sample-approval-sheet.csv">Sample approval sheet</a> · '
        '<a href="/resources/pre-shipment-inspection-checklist.csv">Pre-shipment inspection checklist</a> · '
        '<a href="/resources/purchase-order-checklist.csv">PO checklist</a></div>'
        '</div></section>'
    )


def main():
    cases = {c['n']: c for c in seo.load_cases()}
    assert len(DETAILS) == 10, len(DETAILS)
    changed = 0
    for n, detail in DETAILS.items():
        case = cases.get(n)
        assert case, n
        slug = f"{n}-{seo.slugify(case['title'])}"
        page = seo.PUBLIC / 'case-studies' / slug / 'index.html'
        assert page.is_file(), page
        text = page.read_text(encoding='utf-8')
        if 'data-hero-control-plan' in text:
            continue
        marker = '<section class="band">'
        assert marker in text, page
        text = text.replace(marker, section(detail) + marker, 1)
        page.write_text(text, encoding='utf-8')
        changed += 1

    present = sum(
        1 for p in (seo.PUBLIC / 'case-studies').glob('*/index.html')
        if 'data-hero-control-plan' in p.read_text(encoding='utf-8')
    )
    assert present == 10, present
    print(f'Hero case depth OK: {present} detailed control-plan case pages ({changed} changed)')


if __name__ == '__main__':
    main()
