#!/usr/bin/env python3
from __future__ import annotations
import html,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; PUBLIC=ROOT/'public'; BASE='https://pomerol.trade'
ORG_ID=BASE+'/#organization'; SITE_ID=BASE+'/#website'
LANG_HOMES={'en':'/en/','zh-CN':'/zh/','ja':'/ja/','ru':'/ru/','es':'/es/','pt':'/pt/'}
CASE_HUBS={'en':'/cases/','zh-CN':'/zh/cases/','ja':'/ja/cases/','ru':'/ru/cases/','es':'/es/cases/','pt':'/pt/cases/'}
REPL={'Nicole':'Yusuf','13923387986@163.com':'abd.yusuf.ibrahim.mustafa@gmail.com','+86 139 2338 7986':'+86 132 4269 4270','+8613923387986':'+8613242694270','8613923387986':'8613242694270'}
SITEMAP_LASTMOD={
    BASE+'/en/':'2026-10-04T04:50:28.000Z',
    BASE+'/china-sourcing-agent/':'2026-10-04T04:50:28.000Z',
    BASE+'/china-procurement-services/':'2026-10-04T04:50:28.000Z',
}

def esc(v): return html.escape(str(v),quote=True)
def compact_description(value, limit=160):
    text=re.sub(r'\s+',' ',str(value)).strip()
    if len(text)<=limit: return text
    head=text[:limit-1]
    sentence_matches=list(re.finditer(r'[.!?。！？](?=\s|$)',head))
    sentence_end=sentence_matches[-1].end() if sentence_matches else 0
    word_end=head.rfind(' ')
    cut_at=sentence_end if sentence_end>=80 else word_end if word_end>=80 else limit-1
    return head[:cut_at].rstrip(' \t\r\n,;:—–-')+'…'

def set_meta_description(text, description):
    tag=f'<meta name="description" content="{esc(description)}">'
    pattern=r'<meta\s+name=["\']description["\'][^>]*>'
    if re.search(pattern,text,re.I):
        return re.sub(pattern,lambda _:tag,text,count=1,flags=re.I)
    return re.sub(r'</head>',tag+'\n</head>',text,count=1,flags=re.I)

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
    return {'@type':'Organization','@id':ORG_ID,'name':'Pomerol International','legalName':'Pomerol International Trade (Zhuhai) Co., Ltd.','alternateName':'波美猴国际贸易（珠海）有限公司','url':BASE+'/','logo':BASE+'/assets/logo.svg','email':'abd.yusuf.ibrahim.mustafa@gmail.com','telephone':'+86 132 4269 4270','address':{'@type':'PostalAddress','addressLocality':'Zhuhai','addressRegion':'Guangdong','addressCountry':'CN'},'contactPoint':[{'@type':'ContactPoint','name':'Yusuf','contactType':'sales','email':'contact@pomerol.trade','telephone':'+86 132 4269 4270','availableLanguage':['English','Chinese','Japanese','Russian','Spanish','Portuguese'],'areaServed':'Worldwide'},{'@type':'ContactPoint','name':'Yusuf','contactType':'sales','email':'abd.yusuf.ibrahim.mustafa@gmail.com','telephone':'+86 132 4269 4270','availableLanguage':['English','Chinese','Japanese','Russian','Spanish','Portuguese'],'areaServed':'Worldwide'}],'areaServed':'Worldwide','knowsAbout':['China sourcing','supplier sourcing','procurement','OEM and ODM','quality inspection','factory verification','export coordination','multi-supplier consolidation']}

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
    graph=[org(),website(),{'@type':'WebPage','@id':can+'#webpage','url':can,'name':title,'description':desc,'isPartOf':{'@id':SITE_ID},'about':{'@id':ORG_ID},'inLanguage':language,'primaryImageOfPage':{'@type':'ImageObject','url':img}}]+(extra or [])
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

FOOTER_CONTACT_LABELS = {
    "en": ("Phone / WhatsApp:", "Direct email:", "Business email:"),
    "zh": ("电话 / WhatsApp：", "联系邮箱：", "业务邮箱："),
    "ja": ("電話 / WhatsApp：", "連絡用メール：", "業務用メール："),
    "ru": ("Телефон / WhatsApp:", "Прямой email:", "Рабочий email:"),
    "es": ("Teléfono / WhatsApp:", "Correo directo:", "Correo comercial:"),
    "pt": ("Telefone / WhatsApp:", "E-mail direto:", "E-mail comercial:"),
}


def footer_contact_labels(language):
    code = language.lower().split("-", 1)[0]
    return FOOTER_CONTACT_LABELS.get(code, FOOTER_CONTACT_LABELS["en"])


def label_footer_contacts(text):
    language_match = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', text, re.I)
    labels = footer_contact_labels(language_match.group(1) if language_match else "en")

    def update_footer(match):
        footer = match.group(2)
        targets = (
            ("tel:+8613242694270", labels[0]),
            ("mailto:abd.yusuf.ibrahim.mustafa@gmail.com", labels[1]),
            ("mailto:contact@pomerol.trade", labels[2]),
        )
        for href, label in targets:
            pattern = re.compile(
                r'(<a\b[^>]*\bhref=["\']' + re.escape(href) + r'["\'][^>]*>)(.*?)(</a>)',
                re.I | re.S,
            )

            def add_label(anchor):
                plain = html.unescape(re.sub(r"<[^>]+>", "", anchor.group(2))).strip()
                normalize = lambda value: re.sub(r"[\W_]+", "", value.casefold())
                if normalize(label) in normalize(plain):
                    return anchor.group(0)
                return anchor.group(1) + label + " " + anchor.group(2) + anchor.group(3)

            footer = pattern.sub(add_label, footer)

        if "contact@pomerol.trade" not in footer.casefold():
            direct_email = re.compile(
                r'(<a\b[^>]*\bhref=["\']mailto:abd\.yusuf\.ibrahim\.mustafa@gmail\.com["\'][^>]*>.*?</a>)',
                re.I | re.S,
            )
            if direct_email.search(footer):
                footer = direct_email.sub(
                    r'\1<a href="mailto:contact@pomerol.trade">' + labels[2] + ' contact@pomerol.trade</a>',
                    footer,
                    count=1,
                )
        return match.group(1) + footer + match.group(3)

    return re.sub(r'(<footer\b[^>]*>)([\s\S]*?)(</footer>)', update_footer, text, count=1, flags=re.I)


def inject(p):
    text=p.read_text(encoding='utf-8')
    text=label_footer_contacts(text)
    for a,b in REPL.items(): text=text.replace(a,b)
    text=strip_seo(text); title,desc=title_desc(text); desc=compact_description(desc); text=set_meta_description(text,desc); can=canonical(p); img=image_for(text)
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
def footer(): return '<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="/en/"><img src="/assets/logo.svg" alt=""><span>Pomerol International<small>波美猴国际贸易（珠海）有限公司</small></span></a><p style="max-width:380px;color:#aebccd">China sourcing, procurement, OEM/ODM, quality control and export coordination for overseas buyers.</p></div><div><h4>Core services</h4><a href="/china-sourcing-agent/">China sourcing agent</a><a href="/china-procurement-services/">Procurement services</a><a href="/china-oem-odm-sourcing/">OEM / ODM</a><a href="/china-quality-inspection/">Quality inspection</a></div><div><h4>Industries</h4><a href="/industrial-sourcing-china/">Industrial</a><a href="/electronics-sourcing-china/">Electronics</a><a href="/solar-energy-storage-sourcing-china/">Energy</a><a href="/hotel-supplies-sourcing-china/">Hospitality</a></div><div><h4>Yusuf</h4><a href="tel:+8613242694270">+86 132 4269 4270</a><a href="mailto:contact@pomerol.trade">Business email · contact@pomerol.trade</a><a href="mailto:abd.yusuf.ibrahim.mustafa@gmail.com">abd.yusuf.ibrahim.mustafa@gmail.com</a><a href="https://wa.me/8613242694270">WhatsApp</a></div></div><div class="footer-bottom"><span>© 2026 Pomerol International Trade (Zhuhai) Co., Ltd.</span><span><a style="display:inline" href="/privacy/">Privacy</a> · <a style="display:inline" href="/terms/">Terms</a></span></div></div></footer>'

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
        tool_card = ''
        if s['slug'] == 'china-sourcing-agent':
            tool_card = (
                '<section class="section" aria-labelledby="sourcing-rfq-checklist"><div class="wrap">'
                '<div class="section-head"><div><div class="eyebrow">Buyer readiness</div>'
                '<h2 class="display" id="sourcing-rfq-checklist">A better shortlist starts with a comparable RFQ.</h2></div>'
                '<p>When suppliers receive different assumptions, their prices are not directly comparable. Set the same product, quantity, delivery and acceptance baseline before choosing a supplier.</p></div>'
                '<div class="grid-3">'
                '<article class="card"><h3>1. Define the product</h3><p>Share a specification or drawing revision, material, dimensions, finish, tolerances, reference samples and the features that are fixed versus open to proposal. Mark unresolved points instead of letting each supplier guess.</p></article>'
                '<article class="card"><h3>2. Normalize the commercial basis</h3><p>Request the same quantity tiers, MOQ, tooling or setup cost, sample cost, packaging, lead time, quote validity, payment proposal and delivery term from each candidate. Ask each supplier to list exclusions and assumptions.</p></article>'
                '<article class="card"><h3>3. Set evidence and acceptance rules</h3><p>Identify the target market, buyer-specified documents or tests, sample stages, measurable acceptance criteria and packaging checks. Tie each requested claim to the specific product, supplier entity or manufacturing site it is meant to cover.</p></article>'
                '</div><div class="hero-actions" style="margin-top:24px">'
                '<a class="btn primary" href="/tools/china-rfq-builder/">Build a free supplier RFQ →</a>'
                '<a class="btn light" href="/resources/guides/china-rfq-template-guide/">Read the RFQ preparation guide</a></div>'
                '<p style="color:var(--muted);margin-top:16px">The builder runs in your browser and does not submit or save your inputs. Its checklist helps structure a request; it does not determine legal, customs, safety or certification requirements.</p>'
                '</div></section>'
                '<section class="section dark" aria-labelledby="sourcing-scope-questions"><div class="wrap">'
                '<div class="section-head"><div><div class="eyebrow">Clear scope</div>'
                '<h2 class="display" id="sourcing-scope-questions">Questions to settle before a sourcing engagement.</h2></div></div>'
                '<div class="grid-3">'
                '<article class="card" style="background:#14304f;border-color:rgba(255,255,255,.12)"><h3>Are you the factory?</h3><p class="muted">Pomerol presents its role as China-side sourcing and procurement coordination. Supplier factories are separate businesses; their legal identity, manufacturing role and product capability should be evaluated for the specific project.</p></article>'
                '<article class="card" style="background:#14304f;border-color:rgba(255,255,255,.12)"><h3>Who is responsible for each step?</h3><p class="muted">Before work starts, document who contracts with and pays each supplier, who approves samples and production changes, whether inspections are included or third-party, and who arranges freight and import clearance.</p></article>'
                '<article class="card" style="background:#14304f;border-color:rgba(255,255,255,.12)"><h3>What is included in the fee?</h3><p class="muted">Scope can range from a shortlist or RFQ comparison to ongoing purchase follow-up. Confirm the exact deliverables, timing, third-party charges, exclusions and commercial terms before authorizing project work.</p></article>'
                '</div></div></section>'
            )
        body=f'<section class="page-hero"><div class="wrap page-hero-grid"><div><div class="eyebrow">{esc(s["eyebrow"])}</div><h1 class="display">{esc(s["h1"])}</h1><p>{esc(s["intro"])}</p><div class="hero-actions"><a class="btn primary" href="/contact/">Send an RFQ →</a><a class="btn light" href="/cases/">Browse sourcing scenarios</a></div></div><div><img src="/assets/photos/{esc(s["image"])}" alt="{esc(s["eyebrow"])} in China"></div></div></section><section class="section"><div class="wrap split"><div><div class="eyebrow">Why buyers use us</div><h2 class="display" style="font-size:3rem">The supplier search is only the first control point.</h2><p class="lead">{esc(s["problem"])}</p><p>{esc(s["buyers"])}</p></div><div class="card"><h3>Typical scope</h3><ul>{bullets}</ul></div></div></section><section class="section dark"><div class="wrap"><div class="section-head"><div><div class="eyebrow">Execution model</div><h2 class="display">A defined path from requirement to shipment.</h2></div></div><div class="process">{steps}</div></div></section>{tool_card}<section class="section"><div class="wrap"><div class="section-head"><div><div class="eyebrow">Illustrative scenarios</div><h2 class="display">Sourcing situations buyers may need to control.</h2></div><p>These are illustrative scenarios for explaining sourcing decisions. They are not verified completed customer projects, performance results or endorsements. Client profiles and selected details may be fictionalized; photos show product categories, not customer shipments.</p></div><div class="case-preview-grid">{case_cards(cases,s["case_ids"])}</div></div></section><section class="band"><div class="wrap band-grid"><h2 class="display">Have a product, drawing, BOM or supplier problem? Send it to Yusuf.</h2><div><a class="btn ghost" href="/contact/">Start the sourcing brief →</a></div></div></section>'
        page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(s["title"])} | Pomerol International</title><meta name="description" content="{esc(s["description"])}"><meta name="keywords" content="{esc(s["keywords"])}"><link rel="icon" href="/assets/logo.svg"><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script>{tags}</head><body>{nav()}<main>{body}</main>{footer()}</body></html>'
        d=PUBLIC/s['slug']; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(page,encoding='utf-8')

def build_case_pages(cases):
    for c in cases:
        s=f"{c['n']}-{slugify(c['title'])}"; can=f'{BASE}/case-studies/{s}/'; title=c['title']+' — China Sourcing Scenario'; desc=f'Illustrative {c["industry"].lower()} sourcing scenario for a {c["profile"].lower()} in {c["market"]}: requirements, supplier comparison and buyer control points.'
        article={'@type':'Article','@id':can+'#article','headline':c['title'],'description':desc,'image':f'{BASE}/assets/photos/{c["photo"]}','author':{'@id':ORG_ID},'publisher':{'@id':ORG_ID},'mainEntityOfPage':can,'articleSection':c['industry'],'keywords':c['tags'],'inLanguage':'en'}
        tags=seo_tags(title+' | Pomerol International',desc,can,'en',f'{BASE}/assets/photos/{c["photo"]}',kind='article',extra=[article,crumbs(can,title)]); chips=''.join(f'<span class="chip">{esc(x)}</span>' for x in c['tags'])
        body=f'<section class="page-hero"><div class="wrap page-hero-grid"><div><div class="eyebrow">Illustrative scenario · {esc(c["industry"])}</div><h1 class="display">{esc(c["title"])}</h1><p>{esc(desc)}</p><div class="hero-note"><span>Illustrative buyer profile: {esc(c["profile"])}</span></div></div><div><img src="/assets/photos/{esc(c["photo"])}" alt="{esc(c["industry"])} product category"></div></div></section><section class="section compact"><div class="wrap"><div class="notice-box">This page is an illustrative sourcing scenario, not evidence of a completed customer project, shipment, business result or third-party endorsement. Buyer profile, market, commercial details and outcome are fictionalized or illustrative. Product photography shows a category, not a customer shipment.</div></div></section><section class="section"><div class="wrap detail-grid"><aside class="sticky"><div class="eyebrow">Scenario {esc(c["n"])}</div><h2>{esc(c["sector"])}</h2><ul class="list-clean"><li><strong>Illustrative market</strong><span>{esc(c["market"])}</span></li><li><strong>Product area</strong><span>{esc(c["industry"])}</span></li><li><strong>Illustrative buyer type</strong><span>{esc(c["profile"])}</span></li></ul><div class="chips">{chips}</div></aside><div><div class="case-full"><h2>Example buyer requirement</h2><p>{esc(c["challenge"])}</p></div><div class="case-full"><h2>Possible sourcing workstream</h2><p>{esc(c["work"])}</p></div><div class="case-full"><h2>Buyer control points</h2><p>{esc(c["control"])}</p></div><div class="case-full"><h2>Possible process objective</h2><p>{esc(c["result"])}</p></div></div></div></section><section class="band"><div class="wrap band-grid"><h2 class="display">Working on a similar sourcing problem?</h2><div><a class="btn ghost" href="/contact/">Send it to Yusuf →</a></div></div></section>'
        page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Pomerol International</title><meta name="description" content="{esc(desc)}"><link rel="icon" href="/assets/logo.svg"><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script>{tags}</head><body>{nav()}<main>{body}</main>{footer()}</body></html>'
        d=PUBLIC/'case-studies'/s; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(page,encoding='utf-8')

def link_case_hub(cases):
    p=PUBLIC/'cases'/'index.html'; text=p.read_text(encoding='utf-8')
    if 'data-static-case-index' in text:
        text=text.replace('Indexable case archive','Illustrative sourcing scenario library')
        text=text.replace('Browse individual sourcing case pages.','Browse sourcing scenarios by product and control point.')
        text=text.replace('Each case has a dedicated URL with the challenge, sourcing work, control points and representative result.','Each page describes an illustrative buyer situation and possible sourcing controls. The scenarios are not verified completed customer projects, shipments, results or endorsements.')
        p.write_text(text,encoding='utf-8')
        return
    links=''.join(f'<a href="/case-studies/{c["n"]}-{slugify(c["title"])}/">Case {esc(c["n"])} — {esc(c["title"])}</a>' for c in cases)
    block='<section class="section" data-static-case-index><div class="wrap"><div class="section-head"><div><div class="eyebrow">Illustrative sourcing scenario library</div><h2 class="display">Browse sourcing scenarios by product and control point.</h2></div><p>These pages explain illustrative buyer situations and possible sourcing controls. They are not verified completed customer projects, shipments, results or endorsements.</p></div><div class="case-index">'+links+'</div></div></section>'
    p.write_text(text.replace('</main>',block+'</main>',1),encoding='utf-8')

def misc_files(cases,solutions):
    sol='\n'.join(f'- [{s["title"]}]({BASE}/{s["slug"]}/): {s["description"]}' for s in solutions)
    body='''# Pomerol International

> China-side sourcing, procurement and export coordination for overseas buyers, operated from Zhuhai, Guangdong, China.

## About and services

Pomerol International Trade (Zhuhai) Co., Ltd. publishes support for requirement clarification, supplier sourcing and shortlisting, comparable RFQs, OEM/ODM coordination, sample follow-up, supplier evidence checks, quality checkpoints, multi-supplier consolidation and export handoff.

## Primary pages

- English home: https://pomerol.trade/en/
- About Pomerol: https://pomerol.trade/about/
- Services overview: https://pomerol.trade/services/
'''+sol+'''

## Guides and tools

- Buyer guides: https://pomerol.trade/resources/guides/
- RFQ and sourcing resources: https://pomerol.trade/resources/
- Free China supplier RFQ builder: https://pomerol.trade/tools/china-rfq-builder/

## Illustrative scenario library

- Scenario library: https://pomerol.trade/cases/
- These scenarios are illustrative sourcing playbooks, not evidence of completed customer projects, named clients, shipments or measured results. Product-category photographs are not proof of Pomerol work.

## Scope and evidence

- Published services describe sourcing and coordination support. Suppliers and factories are third parties; do not infer Pomerol owns or operates their manufacturing facilities.
- Supplier checks and inspection coordination do not guarantee product quality, regulatory compliance or delivery outcomes.
- The public pages are the source of truth for current service scope and supported claims.

## Contact

- Contact person: Yusuf
- Phone / WhatsApp: +86 132 4269 4270
- Business email: contact@pomerol.trade
- Direct email: abd.yusuf.ibrahim.mustafa@gmail.com
- English contact: https://pomerol.trade/contact/
- Chinese contact: https://pomerol.trade/zh/contact/
- Contact methods are labeled in all six published languages.

## Machine-readable overview and discovery

- Business overview: https://pomerol.trade/ai-overview.md
- XML sitemap: https://pomerol.trade/sitemap.xml
'''
    (PUBLIC/'llms.txt').write_text(body,encoding='utf-8')
    urls=[]
    for p in sorted(PUBLIC.rglob('*.html')):
        r=p.relative_to(PUBLIC).as_posix()
        if p.name=='404.html' or r=='index.html' or r.startswith(('privacy/','terms/')): continue
        loc=canonical(p); im=image_for(p.read_text(encoding='utf-8')); urls.append((loc,im if '/assets/photos/' in im else None))
    ns='xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'; x=[f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset {ns}>']
    for loc,im in urls:
        lastmod=SITEMAP_LASTMOD.get(loc)
        x.append(f'<url><loc>{esc(loc)}</loc>'+(f'<lastmod>{lastmod}</lastmod>' if lastmod else '')+(f'<image:image><image:loc>{esc(im)}</image:loc></image:image>' if im else '')+'</url>')
    x.append('</urlset>'); (PUBLIC/'sitemap.xml').write_text('\n'.join(x),encoding='utf-8')
    robots = f'''User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Allow: /
Allow: /api/social-image/
Disallow: /api/

User-agent: Googlebot
User-agent: Googlebot-Image
User-agent: Bingbot
User-agent: Slurp
User-agent: DuckDuckBot
User-agent: YandexBot
User-agent: Baiduspider
User-agent: 360Spider
User-agent: Sogou web spider
User-agent: Sogou inst spider
Allow: /
Allow: /api/social-image/
Disallow: /api/

User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Applebot
Allow: /
Allow: /api/social-image/
Disallow: /api/

User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Applebot-Extended
Disallow: /

Sitemap: {BASE}/sitemap.xml
'''
    (PUBLIC/'robots.txt').write_text(robots,encoding='utf-8')

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


