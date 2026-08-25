#!/usr/bin/env python3
from __future__ import annotations
import html, json, re
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'
BASE='https://pomerol.in'
ORG_ID=BASE+'/#organization'
SITE_ID=BASE+'/#website'
GUIDES=json.loads((ROOT/'scripts'/'seo_guides.json').read_text(encoding='utf-8'))

def esc(v): return html.escape(str(v),quote=True)
def slugify(v): return re.sub(r'[^a-z0-9]+','-',v.lower()).strip('-')

def load_cases():
    out=[]
    for i in range(1,5):
        t=(PUBLIC/'assets'/f'cases-part-{i}.js').read_text(encoding='utf-8').strip()
        if i==1:
            raw=t.removeprefix('window.CASE_LIBRARY=').rstrip(';')
        else:
            raw=t.removeprefix('window.CASE_LIBRARY.push(...').rstrip(';')
            if raw.endswith(')'): raw=raw[:-1]
        out+=json.loads(raw)
    return out

def nav():
    return '<header class="nav-shell"><nav class="nav wrap"><a class="brand" href="/en/"><img src="/assets/logo.svg" alt="Pomerol International"><span>Pomerol International<small>China sourcing & procurement</small></span></a><button class="menu-btn" data-menu aria-label="Menu">☰</button><div class="navlinks" data-nav><a href="/china-sourcing-agent/">Sourcing</a><a href="/services/">Services</a><a href="/cases/">Case Library</a><a href="/resources/guides/">Buyer Guides</a><a href="/about/">About</a><a class="nav-cta" href="/contact/">Start an RFQ</a></div></nav></header>'

def footer():
    return '<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="/en/"><img src="/assets/logo.svg" alt=""><span>Pomerol International<small>波美猴国际贸易（珠海）有限公司</small></span></a><p style="max-width:380px;color:#aebccd">China sourcing, procurement, OEM/ODM, quality control and export coordination for overseas buyers.</p></div><div><h4>Core services</h4><a href="/china-sourcing-agent/">China sourcing agent</a><a href="/china-procurement-services/">Procurement services</a><a href="/china-oem-odm-sourcing/">OEM / ODM</a><a href="/china-quality-inspection/">Quality inspection</a></div><div><h4>Buyer resources</h4><a href="/resources/guides/">Buyer guides</a><a href="/resources/">RFQ toolkit</a><a href="/cases/">Case library</a></div><div><h4>Yusuf</h4><a href="tel:+8613242694270">+86 132 4269 4270</a><a href="mailto:abd.yusuf.ibrahim.mustafa@gmail.com">abd.yusuf.ibrahim.mustafa@gmail.com</a><a href="https://wa.me/8613242694270">WhatsApp</a></div></div><div class="footer-bottom"><span>© 2026 Pomerol International Trade (Zhuhai) Co., Ltd.</span><span><a style="display:inline" href="/privacy/">Privacy</a> · <a style="display:inline" href="/terms/">Terms</a></span></div></div></footer>'

def org_schema():
    return {'@type':'Organization','@id':ORG_ID,'name':'Pomerol International','url':BASE+'/','logo':BASE+'/assets/logo.svg','email':'abd.yusuf.ibrahim.mustafa@gmail.com','telephone':'+86 132 4269 4270','address':{'@type':'PostalAddress','addressLocality':'Zhuhai','addressRegion':'Guangdong','addressCountry':'CN'}}

def head(title,desc,url,image,article=False):
    graph=[org_schema(),{'@type':'WebSite','@id':SITE_ID,'url':BASE+'/','name':'Pomerol International','publisher':{'@id':ORG_ID}}, {'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'isPartOf':{'@id':SITE_ID},'about':{'@id':ORG_ID},'inLanguage':'en','primaryImageOfPage':{'@type':'ImageObject','url':image}}]
    if article:
        graph.append({'@type':'Article','@id':url+'#article','headline':title,'description':desc,'image':image,'author':{'@id':ORG_ID},'publisher':{'@id':ORG_ID},'mainEntityOfPage':url,'inLanguage':'en','articleSection':'China Sourcing Buyer Guide'})
    graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Pomerol International','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Buyer Guides','item':BASE+'/resources/guides/'},{'@type':'ListItem','position':3,'name':title,'item':url}] if article else [{'@type':'ListItem','position':1,'name':'Pomerol International','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Buyer Guides','item':url}]})
    data=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':'))
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{esc(url)}"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><meta property="og:site_name" content="Pomerol International"><meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{esc(url)}"><meta property="og:image" content="{esc(image)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{esc(image)}"><link rel="icon" href="/assets/logo.svg"><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script><script type="application/ld+json">{data}</script>'''

def guide_cards():
    return ''.join(f'<article class="card"><div class="eyebrow">Buyer guide</div><h3><a href="/resources/guides/{esc(g["slug"])}/">{esc(g["title"])}</a></h3><p>{esc(g["description"])}</p></article>' for g in GUIDES)

def build_hub():
    url=BASE+'/resources/guides/'
    title='China Sourcing Buyer Guides | Pomerol International'
    desc='Practical buyer guides for sourcing products from China: supplier verification, RFQs, sample approval, inspection, consolidation, OEM/ODM and sourcing cost control.'
    body=f'''<section class="page-hero"><div class="wrap"><div class="eyebrow">Knowledge center</div><h1 class="display">China sourcing buyer guides.</h1><p>Practical operating guides for overseas buyers who need to source, verify, develop, inspect and consolidate products in China. Written around buyer-side control points rather than generic supplier lists.</p></div></section><section class="section"><div class="wrap"><div class="grid-3">{guide_cards()}</div></div></section><section class="band"><div class="wrap band-grid"><h2 class="display">Need help applying the process to a live product or supplier?</h2><div><a class="btn ghost" href="/contact/">Send the brief to Yusuf →</a></div></div></section>'''
    d=PUBLIC/'resources'/'guides'; d.mkdir(parents=True,exist_ok=True)
    (d/'index.html').write_text(f'<!doctype html><html lang="en"><head>{head(title,desc,url,BASE+"/assets/photos/product-development.jpg")}</head><body>{nav()}<main>{body}</main>{footer()}</body></html>',encoding='utf-8')

def build_guides(cases):
    cmap={c['n']:c for c in cases}
    for g in GUIDES:
        url=f'{BASE}/resources/guides/{g["slug"]}/'; image=f'{BASE}/assets/photos/{g["image"]}'
        sections=''.join(f'<section class="service-row"><div class="n">{i:02d}</div><div><h2>{esc(s["h"])}</h2><p>{esc(s["p"])}</p></div></section>' for i,s in enumerate(g['sections'],1))
        checklist=''.join(f'<li>{esc(x)}</li>' for x in g['checklist'])
        related=[]
        for cid in g['cases']:
            c=cmap.get(cid)
            if not c: continue
            slug=f'{c["n"]}-{slugify(c["title"])}'
            related.append(f'<article class="case-preview"><img src="/assets/photos/{esc(c["photo"])}" alt="{esc(c["industry"])} sourcing case" loading="lazy" decoding="async"><div class="case-preview-copy"><div class="meta">{esc(c["industry"])} · {esc(c["market"])}</div><h3><a href="/case-studies/{slug}/">{esc(c["title"])}</a></h3><p>{esc(c["result"])}</p></div></article>')
        body=f'''<article><section class="page-hero"><div class="wrap page-hero-grid"><div><div class="eyebrow">China sourcing buyer guide</div><h1 class="display">{esc(g['h1'])}</h1><p>{esc(g['intro'])}</p><div class="hero-actions"><a class="btn primary" href="/{esc(g['service'])}/">Related sourcing service →</a><a class="btn light" href="/contact/">Ask Yusuf about a project</a></div></div><div><img src="/assets/photos/{esc(g['image'])}" alt="{esc(g['title'])}" loading="eager" fetchpriority="high" decoding="async"></div></div></section><section class="section"><div class="wrap detail-grid"><aside class="sticky"><div class="eyebrow">Buyer control points</div><h2 class="display" style="font-size:2.5rem">A process that can be checked, not guessed.</h2><p>Use this guide as an operating framework and adapt the depth of control to product risk, order value, customization and destination-market requirements.</p><div class="card"><h3>Working checklist</h3><ul>{checklist}</ul></div></aside><div>{sections}</div></div></section><section class="section dark"><div class="wrap"><div class="section-head"><div><div class="eyebrow">Related case evidence</div><h2 class="display">How these control points appear in real sourcing work.</h2></div><p class="muted">Client names and selected commercial details are pseudonymized or illustrative.</p></div><div class="case-preview-grid">{''.join(related)}</div></div></section><section class="band"><div class="wrap band-grid"><h2 class="display">Apply this guide to a real China sourcing project.</h2><div><a class="btn ghost" href="/contact/">Send an RFQ →</a></div></div></section></article>'''
        d=PUBLIC/'resources'/'guides'/g['slug']; d.mkdir(parents=True,exist_ok=True)
        (d/'index.html').write_text(f'<!doctype html><html lang="en"><head>{head(g["title"]+" | Pomerol International",g["description"],url,image,True)}</head><body>{nav()}<main>{body}</main>{footer()}</body></html>',encoding='utf-8')

def inject_links():
    resources=PUBLIC/'resources'/'index.html'; text=resources.read_text(encoding='utf-8')
    if 'data-buyer-guides' not in text:
        block=f'<section class="section" data-buyer-guides><div class="wrap"><div class="section-head"><div><div class="eyebrow">Buyer guides</div><h2 class="display">Practical China sourcing knowledge center.</h2></div><p>Detailed guides for supplier verification, RFQ control, samples, inspection, consolidation, OEM/ODM and sourcing costs.</p></div><div class="grid-3">{guide_cards()}</div><div style="margin-top:24px"><a class="btn light" href="/resources/guides/">View all buyer guides →</a></div></div></section>'
        text=text.replace('</main>',block+'</main>',1); resources.write_text(text,encoding='utf-8')
    for rel in ('index.html','en/index.html'):
        p=PUBLIC/rel; text=p.read_text(encoding='utf-8')
        if '/resources/guides/' not in text:
            block='<section class="section compact"><div class="wrap"><div class="section-head"><div><div class="eyebrow">Buyer knowledge center</div><h2 class="display">Build the sourcing process before the order gets expensive.</h2></div><p>Read practical guides on supplier verification, RFQs, sample approval, inspection, consolidation and OEM/ODM execution.</p></div><div class="case-index"><a href="/resources/guides/how-to-source-products-from-china/">How to source from China</a><a href="/resources/guides/china-supplier-verification-checklist/">Supplier verification checklist</a><a href="/resources/guides/china-rfq-template-guide/">RFQ guide</a><a href="/resources/guides/">All buyer guides →</a></div></div></section>'
            text=text.replace('</main>',block+'</main>',1); p.write_text(text,encoding='utf-8')
    for g in GUIDES:
        p=PUBLIC/g['service']/'index.html'
        if not p.exists(): continue
        text=p.read_text(encoding='utf-8'); href=f'/resources/guides/{g["slug"]}/'
        if href in text: continue
        block=f'<section class="section compact"><div class="wrap"><div class="notice-box"><strong>Buyer guide:</strong> <a class="small-link" href="{href}">{esc(g["title"])}</a> — {esc(g["description"])}</div></div></section>'
        text=text.replace('</main>',block+'</main>',1); p.write_text(text,encoding='utf-8')

def strip_fake_dates():
    for p in PUBLIC.rglob('*.html'):
        text=p.read_text(encoding='utf-8')
        def repl(m):
            try: data=json.loads(m.group(1))
            except Exception: return m.group(0)
            def walk(x):
                if isinstance(x,dict):
                    x.pop('datePublished',None); x.pop('dateModified',None)
                    for v in x.values(): walk(v)
                elif isinstance(x,list):
                    for v in x: walk(v)
            walk(data)
            return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':'))+'</script>'
        text=re.sub(r'<script type="application/ld\+json">(.*?)</script>',repl,text,flags=re.S)
        p.write_text(text,encoding='utf-8')

def rebuild_sitemap():
    rows={}
    for p in PUBLIC.rglob('*.html'):
        text=p.read_text(encoding='utf-8')
        if re.search(r'<meta name="robots" content="noindex',text,re.I): continue
        m=re.search(r'<link rel="canonical" href="([^"]+)"',text,re.I)
        if not m: continue
        url=m.group(1)
        if not url.startswith(BASE): continue
        im=re.search(r'<img[^>]+src="(/assets/photos/[^"]+)"',text,re.I)
        rows[url]=BASE+im.group(1) if im else None
    parts=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for url in sorted(rows):
        parts.append('<url><loc>'+xml_escape(url)+'</loc>')
        if rows[url]: parts.append('<image:image><image:loc>'+xml_escape(rows[url])+'</image:loc></image:image>')
        parts.append('</url>')
    parts.append('</urlset>')
    (PUBLIC/'sitemap.xml').write_text(''.join(parts),encoding='utf-8')

def update_llms():
    p=PUBLIC/'llms.txt'
    text=p.read_text(encoding='utf-8') if p.exists() else '# Pomerol International\n'
    if '/resources/guides/' not in text:
        text += '\n## Buyer Guides\n- https://pomerol.in/resources/guides/\n' + ''.join(f'- https://pomerol.in/resources/guides/{g["slug"]}/ — {g["title"]}\n' for g in GUIDES)
    p.write_text(text,encoding='utf-8')

def main():
    assert len(GUIDES)==8
    cases=load_cases(); assert len(cases)==36
    build_hub(); build_guides(cases); inject_links(); strip_fake_dates(); rebuild_sitemap(); update_llms()
    assert len(list((PUBLIC/'resources'/'guides').glob('*/index.html')))==8
    assert '<lastmod>' not in (PUBLIC/'sitemap.xml').read_text(encoding='utf-8')
    assert 'data-buyer-guides' in (PUBLIC/'resources'/'index.html').read_text(encoding='utf-8')
    print('Buyer guide SEO OK: 8 guides + hub, truthful sitemap, internal links')

if __name__=='__main__': main()
