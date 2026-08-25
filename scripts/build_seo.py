#!/usr/bin/env python3
from __future__ import annotations
import html,json,re
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; PUBLIC=ROOT/'public'; BASE='https://pomerol.in'; TODAY=date.today().isoformat()
ORG_ID=BASE+'/#organization'; SITE_ID=BASE+'/#website'
LANG_HOMES={'en':'/en/','zh-CN':'/zh/','ja':'/ja/','ru':'/ru/','es':'/es/','pt':'/pt/'}
CASE_HUBS={'en':'/cases/','zh-CN':'/zh/cases/','ja':'/ja/cases/','ru':'/ru/cases/','es':'/es/cases/','pt':'/pt/cases/'}
REPL={'Nicole':'Yusuf','13923387986@163.com':'abd.yusuf.ibrahim.mustafa@gmail.com','+86 139 2338 7986':'+86 132 4269 4270','+8613923387986':'+8613242694270','8613923387986':'8613242694270'}

def esc(v): return html.escape(str(v),quote=True)
def slugify(v): return re.sub(r'[^a-z0-9]+','-',v.lower()).strip('-')
def load_solutions():
    out=[]
    for name in ('seo_pages_core.json','seo_pages_industries.json'):
        out+=json.loads((ROOT/'scripts'/name).read_text(encoding='utf-8'))
    return out

def load_cases():
    out=[]
    for i in range(1,5):
        t=(PUBLIC/'assets'/f'cases-part-{i}.js').read_text(encoding='utf-8').strip()
        if i==1: p=t.removeprefix('window.CASE_LIBRARY=').rstrip(';')
        else:
            p=t.removeprefix('window.CASE_LIBRARY.push(...').rstrip(';')
            if p.endswith(')'): p=p[:-1]
        out+=json.loads(p)
    return out

def lang(rel):
    for p,l in [('zh/','zh-CN'),('ja/','ja'),('ru/','ru'),('es/','es'),('pt/','pt')]:
        if rel.startswith(p): return l
    return 'en'

def url_for(p):
    r=p.relative_to(PUBLIC).as_posix()
    if r=='index.html': return BASE+'/'
    if r.endswith('/index.html'): return BASE+'/'+r[:-10]
    return BASE+'/'+r

def canonical(p): return BASE+'/en/' if p.relative_to(PUBLIC).as_posix()=='index.html' else url_for(p)
def image_for(text):
    m=re.search(r'<img[^>]+src="(/assets/photos/[^"]+)"',text,re.I)
    return BASE+m.group(1) if m else BASE+'/assets/logo.svg'

def org():
    return {'@type':'Organization','@id':ORG_ID,'name':'Pomerol International','legalName':'Pomerol International Trade (Zhuhai) Co., Ltd.','alternateName':'波美猴国际贸易（珠海）有限公司','url':BASE+'/','logo':BASE+'/assets/logo.svg','email':'abd.yusuf.ibrahim.mustafa@gmail.com','telephone':'+86 132 4269 4270','address':{'@type':'PostalAddress','addressLocality':'Zhuhai','addressRegion':'Guangdong','addressCountry':'CN'},'contactPoint':{'@type':'ContactPoint','name':'Yusuf','contactType':'sales','email':'abd.yusuf.ibrahim.mustafa@gmail.com','telephone':'+86 132 4269 4270','availableLanguage':['English','Chinese','Japanese','Russian','Spanish','Portuguese'],'areaServed':'Worldwide'},'areaServed':'Worldwide','knowsAbout':['China sourcing','supplier sourcing','procurement','OEM and ODM','quality inspection','factory verification','export coordination','multi-supplier consolidation']}

def website(): return {'@type':'WebSite','@id':SITE_ID,'url':BASE+'/','name':'Pomerol International','alternateName':'Pomerol China Sourcing','publisher':{'@id':ORG_ID},'inLanguage':['en','zh-CN','ja','ru','es','pt']}

def crumbs(url,title):
    path=url.removeprefix(BASE).strip('/'); items=[{'@type':'ListItem','position':1,'name':'Pomerol International','item':BASE+'/'}]
    acc=''; parts=path.split('/') if path else []
    for i,part in enumerate(parts,start=2):
        acc+='/'+part; label=title if i==len(parts)+1 else part.replace('-',' ').title(); items.append({'@type':'ListItem','position':i,'name':label,'item':BASE+acc+'/'})
    return {'@type':'BreadcrumbList','itemListElement':items}

def seo_tags(title,desc,can,language,img,kind='website',alts=None,extra=None):
    links=[]
    for code,href in (alts or {}).items(): links.append(f'<link rel="alternate" hreflang="{esc(code)}" href="{esc(BASE+href)}">')
    graph=[org(),website(),{'@type':'WebPage','@id':can+'#webpage','url':can,'name':title,'description':desc,'isPartOf':{'@id':SITE_ID},'about':{'@id':ORG_ID},'inLanguage':language,'primaryImageOfPage':{'@type':'ImageObject','url':img},'dateModified':TODAY}]+(extra or [])
    data=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':'))
    return '\n'.join([f'<link rel="canonical" href="{esc(can)}">',*links,'<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">','<meta property="og:site_name" content="Pomerol International">',f'<meta property="og:type" content="{kind}">',f'<meta property="og:title" content="{esc(title)}">',f'<meta property="og:description" content="{esc(desc)}">',f'<meta property="og:url" content="{esc(can)}">',f'<meta property="og:image" content="{esc(img)}">','<meta name="twitter:card" content="summary_large_image">',f'<meta name="twitter:title" content="{esc(title)}">',f'<meta name="twitter:description" content="{esc(desc)}">',f'<meta name="twitter:image" content="{esc(img)}">',f'<script type="application/ld+json">{data}</script>'])

def strip_seo(text):
    pats=[r'<link rel="canonical"[^>]*>\s*',r'<link rel="alternate" hreflang="[^"]+"[^>]*>\s*',r'<meta name="robots"[^>]*>\s*',r'<meta property="og:(?:site_name|type|title|description|url|image)"[^>]*>\s*',r'<meta name="twitter:(?:card|title|description|image)"[^>]*>\s*',r'<script type="application/ld\+json">.*?</script>\s*']
    for p in pats: text=re.sub(p,'',text,flags=re.I|re.S)
    return text

def title_desc(text):
    tm=re.search(r'<title>(.*?)</title>',text,re.I|re.S); dm=re.search(r'<meta name="description" content="([^"]*)"',text,re.I)
    return (html.unescape(tm.group(1).strip()) if tm else 'Pomerol International',html.unescape(dm.group(1).strip()) if dm else 'China sourcing, procurement, supplier control and export coordination for overseas buyers.')

def hreflang(p):
    r=p.relative_to(PUBLIC).as_posix()
    if r in {'index.html','en/index.html','zh/index.html','ja/index.html','ru/index.html','es/index.html','pt/index.html'}: d=dict(LANG_HOMES); d['x-default']='/en/'; return d
    if r in {'cases/index.html','zh/cases/index.html','ja/cases/index.html','ru/cases/index.html','es/cases/index.html','pt/cases/index.html'}: d=dict(CASE_HUBS); d['x-default']='/cases/'; return d
    return None

def inject(p):
    text=p.read_text(encoding='utf-8')
    for a,b in REPL.items(): text=text.replace(a,b)
    text=strip_seo(text); title,desc=title_desc(text); can=canonical(p); img=image_for(text)
    if p.name=='404.html': text=text.replace('</head>','<meta name="robots" content="noindex,follow"></head>')
    else: text=text.replace('</head>',seo_tags(title,desc,can,lang(p.relative_to(PUBLIC).as_posix()),img,alts=hreflang(p),extra=[crumbs(can,title)])+'\n</head>',1)
    seen=False
    def repl(m):
        nonlocal seen; tag=m.group(0)
        if 'loading=' in tag or 'src="/assets/photos/' not in tag: return tag
        if not seen: seen=True; return tag[:-1]+' loading="eager" fetchpriority="high" decoding="async">'
        return tag[:-1]+' loading="lazy" decoding="async">'
    p.write_text(re.sub(r'<img\b[^>]*>',repl,text,flags=re.I),encoding='utf-8')

def nav(): return '<header class="nav-shell"><nav class="nav wrap"><a class="brand" href="/en/"><img src="/assets/logo.svg" alt="Pomerol International"><span>Pomerol International<small>China sourcing & procurement</small></span></a><button class="menu-btn" data-menu aria-label="Menu">☰</button><div class="navlinks" data-nav><a href="/china-sourcing-agent/">Sourcing</a><a href="/services/">Services</a><a href="/cases/">Case Library</a><a href="/about/">About</a><a href="/resources/">Resources</a><a class="nav-cta" href="/contact/">Start an RFQ</a></div></nav></header>'
def footer(): return '<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="/en/"><img src="/assets/logo.svg" alt=""><span>Pomerol International<small>波美猴国际贸易（珠海）有限公司</small></span></a><p style="max-width:380px;color:#aebccd">China sourcing, procurement, OEM/ODM, quality control and export coordination for overseas buyers.</p></div><div><h4>Core services</h4><a href="/china-sourcing-agent/">China sourcing agent</a><a href="/china-procurement-services/">Procurement services</a><a href="/china-oem-odm-sourcing/">OEM / ODM</a><a href="/china-quality-inspection/">Quality inspection</a></div><div><h4>Industries</h4><a href="/industrial-sourcing-china/">Industrial</a><a href="/electronics-sourcing-china/">Electronics</a><a href="/solar-energy-storage-sourcing-china/">Energy</a><a href="/hotel-supplies-sourcing-china/">Hospitality</a></div><div><h4>Yusuf</h4><a href="tel:+8613242694270">+86 132 4269 4270</a><a href="mailto:abd.yusuf.ibrahim.mustafa@gmail.com">abd.yusuf.ibrahim.mustafa@gmail.com</a><a href="https://wa.me/8613242694270">WhatsApp</a></div></div><div class="footer-bottom"><span>© 2026 Pomerol International Trade (Zhuhai) Co., Ltd.</span><span><a style="display:inline" href="/privacy/">Privacy</a> · <a style="display:inline" href="/terms/">Terms</a></span></div></div></footer>'

def case_cards(cases,ids):
    out=[]
    for c in [c for c in cases if c['n'] in ids][:6]:
        s=f"{c['n']}-{slugify(c['title'])}"; out.append(f'<article class="case-preview"><img src="/assets/photos/{esc(c["photo"])}" alt="{esc(c["industry"])} sourcing case" loading="lazy" decoding="async"><div class="case-preview-copy"><div class="meta">{esc(c["industry"])} · {esc(c["market"])}</div><h3><a href="/case-studies/{s}/">{esc(c["title"])}</a></h3><p>{esc(c["challenge"])}</p></div></article>')
    return ''.join(out)

def build_solution_pages(cases,solutions):
    for s in solutions:
        can=f"{BASE}/{s['slug']}/"; service={'@type':'Service','@id':can+'#service','name':s['title'],'description':s['description'],'provider':{'@id':ORG_ID},'areaServed':'Worldwide','serviceType':s['title'],'url':can}
        tags=seo_tags(s['title']+' | Pomerol International',s['description'],can,'en',f"{BASE}/assets/photos/{s['image']}",extra=[service,crumbs(can,s['title'])])
        bullets=''.join('<li>'+esc(x)+'</li>' for x in s['scope']); steps=''.join(f'<div class="step"><b>{i:02d}</b><h3>{esc(x)}</h3></div>' for i,x in enumerate(s['workflow'],1))
        body=f'<section class="page-hero"><div class="wrap page-hero-grid"><div><div class="eyebrow">{esc(s["eyebrow"])}</div><h1 class="display">{esc(s["h1"])}</h1><p>{esc(s["intro"])}</p><div class="hero-actions"><a class="btn primary" href="/contact/">Send an RFQ →</a><a class="btn light" href="/cases/">View case studies</a></div></div><div><img src="/assets/photos/{esc(s["image"])}" alt="{esc(s["eyebrow"])} in China"></div></div></section><section class="section"><div class="wrap split"><div><div class="eyebrow">Why buyers use us</div><h2 class="display" style="font-size:3rem">The supplier search is only the first control point.</h2><p class="lead">{esc(s["problem"])}</p><p>{esc(s["buyers"])}</p></div><div class="card"><h3>Typical scope</h3><ul>{bullets}</ul></div></div></section><section class="section dark"><div class="wrap"><div class="section-head"><div><div class="eyebrow">Execution model</div><h2 class="display">A defined path from requirement to shipment.</h2></div></div><div class="process">{steps}</div></div></section><section class="section"><div class="wrap"><div class="section-head"><div><div class="eyebrow">Relevant work</div><h2 class="display">Representative sourcing cases.</h2></div><p>Client names and selected commercial details are pseudonymized or illustrative.</p></div><div class="case-preview-grid">{case_cards(cases,s["case_ids"])}</div></div></section><section class="band"><div class="wrap band-grid"><h2 class="display">Have a product, drawing, BOM or supplier problem? Send it to Yusuf.</h2><div><a class="btn ghost" href="/contact/">Start the sourcing brief →</a></div></div></section>'
        page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(s["title"])} | Pomerol International</title><meta name="description" content="{esc(s["description"])}"><meta name="keywords" content="{esc(s["keywords"])}"><link rel="icon" href="/assets/logo.svg"><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script>{tags}</head><body>{nav()}<main>{body}</main>{footer()}</body></html>'
        d=PUBLIC/s['slug']; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(page,encoding='utf-8')

def build_case_pages(cases):
    for c in cases:
        s=f"{c['n']}-{slugify(c['title'])}"; can=f'{BASE}/case-studies/{s}/'; title=c['title']+' — China Sourcing Case'; desc=f'Representative {c["industry"].lower()} sourcing case for a {c["profile"].lower()} in {c["market"]}: supplier work, controls and outcome.'
        article={'@type':'Article','@id':can+'#article','headline':c['title'],'description':desc,'image':f'{BASE}/assets/photos/{c["photo"]}','author':{'@id':ORG_ID},'publisher':{'@id':ORG_ID},'mainEntityOfPage':can,'datePublished':TODAY,'dateModified':TODAY,'articleSection':c['industry'],'keywords':c['tags'],'inLanguage':'en'}
        tags=seo_tags(title+' | Pomerol International',desc,can,'en',f'{BASE}/assets/photos/{c["photo"]}',kind='article',extra=[article,crumbs(can,title)]); chips=''.join(f'<span class="chip">{esc(x)}</span>' for x in c['tags'])
        body=f'<section class="page-hero"><div class="wrap page-hero-grid"><div><div class="eyebrow">{esc(c["industry"])} · {esc(c["market"])}</div><h1 class="display">{esc(c["title"])}</h1><p>{esc(desc)}</p><div class="hero-note"><span>Client pseudonym: {esc(c["client"])}</span><span>{esc(c["profile"])}</span></div></div><div><img src="/assets/photos/{esc(c["photo"])}" alt="{esc(c["industry"])} sourcing case"></div></div></section><section class="section compact"><div class="wrap"><div class="notice-box">Transparency note: the client name and selected commercial details are pseudonymized or illustrative. The sourcing risks and control methods are representative examples, not third-party endorsements.</div></div></section><section class="section"><div class="wrap detail-grid"><aside class="sticky"><div class="eyebrow">Case {esc(c["n"])}</div><h2>{esc(c["sector"])}</h2><ul class="list-clean"><li><strong>Market</strong><span>{esc(c["market"])}</span></li><li><strong>Industry</strong><span>{esc(c["industry"])}</span></li><li><strong>Client profile</strong><span>{esc(c["profile"])}</span></li></ul><div class="chips">{chips}</div></aside><div><div class="case-full"><h2>Buyer challenge</h2><p>{esc(c["challenge"])}</p></div><div class="case-full"><h2>China-side sourcing work</h2><p>{esc(c["work"])}</p></div><div class="case-full"><h2>Control points</h2><p>{esc(c["control"])}</p></div><div class="case-full"><h2>Representative outcome</h2><p>{esc(c["result"])}</p></div></div></div></section><section class="band"><div class="wrap band-grid"><h2 class="display">Working on a similar sourcing problem?</h2><div><a class="btn ghost" href="/contact/">Send it to Yusuf →</a></div></div></section>'
        page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Pomerol International</title><meta name="description" content="{esc(desc)}"><link rel="icon" href="/assets/logo.svg"><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script>{tags}</head><body>{nav()}<main>{body}</main>{footer()}</body></html>'
        d=PUBLIC/'case-studies'/s; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(page,encoding='utf-8')

def link_case_hub(cases):
    p=PUBLIC/'cases'/'index.html'; text=p.read_text(encoding='utf-8')
    if 'data-static-case-index' in text: return
    links=''.join(f'<a href="/case-studies/{c["n"]}-{slugify(c["title"])}/">Case {esc(c["n"])} — {esc(c["title"])}</a>' for c in cases)
    block='<section class="section" data-static-case-index><div class="wrap"><div class="section-head"><div><div class="eyebrow">Indexable case archive</div><h2 class="display">Browse individual sourcing case pages.</h2></div><p>Each case has a dedicated URL with the challenge, sourcing work, control points and representative result.</p></div><div class="case-index">'+links+'</div></div></section>'
    p.write_text(text.replace('</main>',block+'</main>',1),encoding='utf-8')

def misc_files(cases,solutions):
    sol='\n'.join(f'- [{s["title"]}]({BASE}/{s["slug"]}/): {s["description"]}' for s in solutions); cs='\n'.join(f'- [Case {c["n"]}: {c["title"]}]({BASE}/case-studies/{c["n"]}-{slugify(c["title"])}/)' for c in cases)
    (PUBLIC/'llms.txt').write_text('# Pomerol International\n\n> China sourcing, procurement, OEM/ODM, supplier control, quality inspection, consolidation and export coordination from Zhuhai, Guangdong, China.\n\nContact: Yusuf — abd.yusuf.ibrahim.mustafa@gmail.com — +86 132 4269 4270\n\n## Core service pages\n'+sol+'\n\n## Representative case archive\n'+cs+'\n',encoding='utf-8')
    urls=[]
    for p in sorted(PUBLIC.rglob('*.html')):
        r=p.relative_to(PUBLIC).as_posix()
        if p.name=='404.html' or r=='index.html' or r.startswith(('privacy/','terms/')): continue
        loc=canonical(p); im=image_for(p.read_text(encoding='utf-8')); urls.append((loc,im if '/assets/photos/' in im else None))
    ns='xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'; x=[f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset {ns}>']
    for loc,im in urls: x.append(f'<url><loc>{esc(loc)}</loc><lastmod>{TODAY}</lastmod>'+(f'<image:image><image:loc>{esc(im)}</image:loc></image:image>' if im else '')+'</url>')
    x.append('</urlset>'); (PUBLIC/'sitemap.xml').write_text('\n'.join(x),encoding='utf-8'); (PUBLIC/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n',encoding='utf-8')

def main():
    cases=load_cases(); solutions=load_solutions()
    if len(cases)!=36 or len(solutions)!=14: raise SystemExit(f'Expected 36 cases/14 solutions, got {len(cases)}/{len(solutions)}')
    build_solution_pages(cases,solutions); build_case_pages(cases); link_case_hub(cases)
    for p in sorted(PUBLIC.rglob('*.html')): inject(p)
    misc_files(cases,solutions)
    if len(list((PUBLIC/'case-studies').glob('*/index.html')))!=36: raise SystemExit('case generation failed')
    for p in PUBLIC.rglob('*.html'):
        if p.name!='404.html' and 'rel="canonical"' not in p.read_text(encoding='utf-8'): raise SystemExit(f'missing canonical: {p}')
    print(f'SEO build OK: {len(list(PUBLIC.rglob("*.html")))} HTML, 36 case pages, 14 solution pages')
if __name__=='__main__': main()
