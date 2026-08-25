#!/usr/bin/env python3
from __future__ import annotations
import html,json,re
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'; BASE='https://pomerol.in'; ORG_ID=BASE+'/#organization'; SITE_ID=BASE+'/#website'
EN={g['slug']:g for g in json.loads((ROOT/'scripts'/'seo_guides.json').read_text(encoding='utf-8'))}
PRIORITY=['how-to-source-products-from-china','china-supplier-verification-checklist','china-rfq-template-guide','china-pre-shipment-inspection-guide']
LOCALES={
 'zh':{'lang':'zh-CN','name':'中文','home':'/zh/','hub':'/zh/resources/guides/','eyebrow':'中国采购买方指南','hub_h1':'中国采购买方指南','hub_intro':'面向海外买家的实操知识中心：从供应商开发、核验和 RFQ，到样品、验货与交付控制。','service':'相关采购服务（英文）','contact':'联系 Yusuf','cases':'相关案例（英文详情）','all':'全部指南','control':'买方控制点','control_intro':'把本指南作为操作框架，并根据产品风险、订单金额、定制程度和目标市场要求调整控制深度。','check':'工作清单','apply':'把这套方法用于真实的中国采购项目。'},
 'ja':{'lang':'ja','name':'日本語','home':'/ja/','hub':'/ja/resources/guides/','eyebrow':'中国調達バイヤーガイド','hub_h1':'中国調達バイヤーガイド','hub_intro':'海外バイヤー向けの実務ナレッジセンター。サプライヤー開拓・確認、RFQ、サンプル、検品、出荷管理までを体系化します。','service':'関連サービス（英語）','contact':'Yusuf に相談','cases':'関連事例（詳細は英語）','all':'すべてのガイド','control':'バイヤー側の管理ポイント','control_intro':'このガイドを運用フレームとして、製品リスク、注文金額、カスタム度、仕向市場に応じて管理の深さを調整してください。','check':'実務チェックリスト','apply':'この方法を実際の中国調達案件に適用する。'},
 'ru':{'lang':'ru','name':'Русский','home':'/ru/','hub':'/ru/resources/guides/','eyebrow':'Руководство покупателя по закупкам в Китае','hub_h1':'Руководства по закупкам в Китае','hub_intro':'Практическая база знаний для зарубежных покупателей: поиск и проверка поставщиков, RFQ, образцы, инспекция и контроль отгрузки.','service':'Связанная услуга (англ.)','contact':'Связаться с Yusuf','cases':'Связанные кейсы (подробности на англ.)','all':'Все руководства','control':'Контрольные точки покупателя','control_intro':'Используйте руководство как операционную основу и меняйте глубину контроля в зависимости от риска продукта, стоимости заказа, кастомизации и требований рынка.','check':'Рабочий чек-лист','apply':'Применить этот подход к реальному проекту закупки в Китае.'},
 'es':{'lang':'es','name':'Español','home':'/es/','hub':'/es/resources/guides/','eyebrow':'Guía del comprador para China','hub_h1':'Guías para comprar y abastecerse en China','hub_intro':'Centro práctico para compradores internacionales: búsqueda y verificación de proveedores, RFQ, muestras, inspección y control del embarque.','service':'Servicio relacionado (inglés)','contact':'Hablar con Yusuf','cases':'Casos relacionados (detalle en inglés)','all':'Todas las guías','control':'Puntos de control del comprador','control_intro':'Use esta guía como marco operativo y ajuste la profundidad del control según riesgo del producto, valor del pedido, personalización y requisitos del mercado destino.','check':'Checklist de trabajo','apply':'Aplicar este método a un proyecto real de sourcing en China.'},
 'pt':{'lang':'pt','name':'Português','home':'/pt/','hub':'/pt/resources/guides/','eyebrow':'Guia do comprador para China','hub_h1':'Guias para compras e sourcing na China','hub_intro':'Centro prático para compradores internacionais: busca e verificação de fornecedores, RFQ, amostras, inspeção e controle de embarque.','service':'Serviço relacionado (inglês)','contact':'Falar com Yusuf','cases':'Casos relacionados (detalhes em inglês)','all':'Todos os guias','control':'Pontos de controle do comprador','control_intro':'Use este guia como estrutura operacional e ajuste a profundidade do controle conforme risco do produto, valor do pedido, customização e requisitos do mercado de destino.','check':'Checklist de trabalho','apply':'Aplicar este método a um projeto real de sourcing na China.'}
}

def esc(v): return html.escape(str(v),quote=True)
def slugify(v): return re.sub(r'[^a-z0-9]+','-',v.lower()).strip('-')

def load_locale(code,slug):
    p=ROOT/'scripts'/'guide_locales'/code/f'{slug}.json'
    if not p.is_file(): raise RuntimeError(f'Missing {p}')
    return json.loads(p.read_text(encoding='utf-8'))

def load_cases():
    out=[]
    for i in range(1,5):
        t=(PUBLIC/'assets'/f'cases-part-{i}.js').read_text(encoding='utf-8').strip()
        if i==1: raw=t.removeprefix('window.CASE_LIBRARY=').rstrip(';')
        else:
            raw=t.removeprefix('window.CASE_LIBRARY.push(...').rstrip(';')
            if raw.endswith(')'): raw=raw[:-1]
        out+=json.loads(raw)
    return {c['n']:c for c in out}

def org_schema():
    return {'@type':'Organization','@id':ORG_ID,'name':'Pomerol International','url':BASE+'/','logo':BASE+'/assets/logo.svg','email':'abd.yusuf.ibrahim.mustafa@gmail.com','telephone':'+86 132 4269 4270','address':{'@type':'PostalAddress','addressLocality':'Zhuhai','addressRegion':'Guangdong','addressCountry':'CN'}}

def cluster(slug=None):
    if slug:
        d={'en':f'/resources/guides/{slug}/','zh-CN':f'/zh/resources/guides/{slug}/','ja':f'/ja/resources/guides/{slug}/','ru':f'/ru/resources/guides/{slug}/','es':f'/es/resources/guides/{slug}/','pt':f'/pt/resources/guides/{slug}/'}
    else:
        d={'en':'/resources/guides/','zh-CN':'/zh/resources/guides/','ja':'/ja/resources/guides/','ru':'/ru/resources/guides/','es':'/es/resources/guides/','pt':'/pt/resources/guides/'}
    d['x-default']=d['en']; return d

def alternates(slug=None): return ''.join(f'<link rel="alternate" hreflang="{k}" href="{BASE+v}">' for k,v in cluster(slug).items())

def lang_switch(slug):
    labels={'en':'English','zh-CN':'中文','ja':'日本語','ru':'Русский','es':'Español','pt':'Português'}
    return '<div class="case-index">'+''.join(f'<a href="{v}">{labels[k]}</a>' for k,v in cluster(slug).items() if k!='x-default')+'</div>'

def nav(code):
    l=LOCALES[code]
    return f'<header class="nav-shell"><nav class="nav wrap"><a class="brand" href="{l["home"]}"><img src="/assets/logo.svg" alt="Pomerol International"><span>Pomerol International<small>China sourcing & procurement</small></span></a><button class="menu-btn" data-menu aria-label="Menu">☰</button><div class="navlinks" data-nav><a href="{l["hub"]}">{esc(l["all"])}</a><a href="/{code}/cases/">Cases</a><a href="{l["home"]}">{esc(l["name"])}</a><a class="nav-cta" href="/contact/">{esc(l["contact"])}</a></div></nav></header>'

def footer(code):
    l=LOCALES[code]
    return f'<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="{l["home"]}"><img src="/assets/logo.svg" alt=""><span>Pomerol International<small>波美猴国际贸易（珠海）有限公司</small></span></a></div><div><h4>{esc(l["all"])}</h4><a href="{l["hub"]}">{esc(l["hub_h1"])}</a><a href="/{code}/cases/">Case Library</a></div><div><h4>Yusuf</h4><a href="tel:+8613242694270">+86 132 4269 4270</a><a href="mailto:abd.yusuf.ibrahim.mustafa@gmail.com">abd.yusuf.ibrahim.mustafa@gmail.com</a><a href="https://wa.me/8613242694270">WhatsApp</a></div></div></div></footer>'

def head(code,slug,title,desc,image,hub=False):
    l=LOCALES[code]; url=BASE+(l['hub'] if hub else f'/{code}/resources/guides/{slug}/')
    graph=[org_schema(),{'@type':'WebSite','@id':SITE_ID,'url':BASE+'/','name':'Pomerol International','publisher':{'@id':ORG_ID}}, {'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'isPartOf':{'@id':SITE_ID},'about':{'@id':ORG_ID},'inLanguage':l['lang'],'primaryImageOfPage':{'@type':'ImageObject','url':image}}]
    if not hub: graph.append({'@type':'Article','@id':url+'#article','headline':title,'description':desc,'image':image,'author':{'@id':ORG_ID},'publisher':{'@id':ORG_ID},'mainEntityOfPage':url,'inLanguage':l['lang'],'articleSection':'China Sourcing Buyer Guide'})
    data=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':'))
    return f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">{alternates(None if hub else slug)}<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><meta property="og:type" content="{"website" if hub else "article"}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{image}"><link rel="icon" href="/assets/logo.svg"><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script><script type="application/ld+json">{data}</script>'

def build_pages(cases):
    for code,l in LOCALES.items():
        cards=[]
        for slug in PRIORITY:
            t=load_locale(code,slug); cards.append(f'<article class="card"><div class="eyebrow">{esc(l["eyebrow"])}</div><h3><a href="/{code}/resources/guides/{slug}/">{esc(t["title"])}</a></h3><p>{esc(t["description"])}</p></article>')
        hub_body=f'<section class="page-hero"><div class="wrap"><div class="eyebrow">{esc(l["eyebrow"])}</div><h1 class="display">{esc(l["hub_h1"])}</h1><p>{esc(l["hub_intro"])}</p>{lang_switch("") .replace("//","/") if False else ""}</div></section><section class="section"><div class="wrap"><div class="grid-2">{"".join(cards)}</div><div style="margin-top:24px"><a class="btn light" href="/resources/guides/">English: all 8 buyer guides →</a></div></div></section>'
        hub_url=BASE+l['hub']; hub_image=BASE+'/assets/photos/product-development.jpg'
        d=PUBLIC/code/'resources'/'guides'; d.mkdir(parents=True,exist_ok=True)
        (d/'index.html').write_text(f'<!doctype html><html lang="{l["lang"]}"><head>{head(code,"",l["hub_h1"]+" | Pomerol International",l["hub_intro"],hub_image,True)}</head><body>{nav(code)}<main>{hub_body}</main>{footer(code)}</body></html>',encoding='utf-8')
        for slug in PRIORITY:
            en=EN[slug]; t=load_locale(code,slug); image=f'{BASE}/assets/photos/{en["image"]}'
            sections=''.join(f'<section class="service-row"><div class="n">{i:02d}</div><div><h2>{esc(s["h"])}</h2><p>{esc(s["p"])}</p></div></section>' for i,s in enumerate(t['sections'],1))
            checklist=''.join(f'<li>{esc(x)}</li>' for x in t['checklist'])
            related=[]
            for cid in en['cases']:
                c=cases.get(cid)
                if not c: continue
                cs=f'{c["n"]}-{slugify(c["title"])}'; related.append(f'<article class="case-preview"><img src="/assets/photos/{esc(c["photo"])}" alt="{esc(c["industry"])}" loading="lazy" decoding="async"><div class="case-preview-copy"><div class="meta">{esc(c["industry"])} · {esc(c["market"])}</div><h3><a href="/case-studies/{cs}/">{esc(c["title"])}</a></h3><p>{esc(c["result"])}</p></div></article>')
            body=f'<article><section class="page-hero"><div class="wrap page-hero-grid"><div><div class="eyebrow">{esc(l["eyebrow"])}</div><h1 class="display">{esc(t["h1"])}</h1><p>{esc(t["intro"])}</p>{lang_switch(slug)}<div class="hero-actions"><a class="btn primary" href="/{en["service"]}/">{esc(l["service"])}</a><a class="btn light" href="/contact/">{esc(l["contact"])}</a></div></div><div><img src="/assets/photos/{esc(en["image"])}" alt="{esc(t["title"])}" loading="eager" fetchpriority="high" decoding="async"></div></div></section><section class="section"><div class="wrap detail-grid"><aside class="sticky"><div class="eyebrow">{esc(l["control"])}</div><p>{esc(l["control_intro"])}</p><div class="card"><h3>{esc(l["check"])}</h3><ul>{checklist}</ul></div></aside><div>{sections}</div></div></section><section class="section dark"><div class="wrap"><div class="section-head"><div><div class="eyebrow">{esc(l["cases"])}</div></div></div><div class="case-preview-grid">{"".join(related)}</div></div></section><section class="band"><div class="wrap band-grid"><h2 class="display">{esc(l["apply"])}</h2><div><a class="btn ghost" href="/contact/">{esc(l["contact"])}</a></div></div></section></article>'
            gd=d/slug; gd.mkdir(parents=True,exist_ok=True)
            url=f'{BASE}/{code}/resources/guides/{slug}/'
            (gd/'index.html').write_text(f'<!doctype html><html lang="{l["lang"]}"><head>{head(code,slug,t["title"]+" | Pomerol International",t["description"],image)}</head><body>{nav(code)}<main>{body}</main>{footer(code)}</body></html>',encoding='utf-8')

def patch_english_hreflang():
    targets=[(PUBLIC/'resources'/'guides'/'index.html',None)]+[(PUBLIC/'resources'/'guides'/s/'index.html',s) for s in PRIORITY]
    for p,slug in targets:
        text=p.read_text(encoding='utf-8')
        text=re.sub(r'<link rel="alternate" hreflang="(?:en|zh-CN|ja|ru|es|pt|x-default)"[^>]*>','',text)
        text=text.replace('</head>',alternates(slug)+'</head>',1)
        p.write_text(text,encoding='utf-8')

def patch_local_homes():
    for code,l in LOCALES.items():
        p=PUBLIC/code/'index.html'; text=p.read_text(encoding='utf-8')
        if f'{l["hub"]}' in text: continue
        cards=''.join(f'<a href="/{code}/resources/guides/{s}/">{esc(load_locale(code,s)["title"])}</a>' for s in PRIORITY)
        block=f'<section class="section compact"><div class="wrap"><div class="section-head"><div><div class="eyebrow">{esc(l["eyebrow"])}</div><h2 class="display">{esc(l["hub_h1"])}</h2></div><p>{esc(l["hub_intro"])}</p></div><div class="case-index">{cards}<a href="{l["hub"]}">{esc(l["all"])} →</a></div></div></section>'
        text=text.replace('</main>',block+'</main>',1); p.write_text(text,encoding='utf-8')

def rebuild_sitemap():
    rows={}
    for p in PUBLIC.rglob('*.html'):
        text=p.read_text(encoding='utf-8')
        if re.search(r'<meta name="robots" content="noindex',text,re.I): continue
        m=re.search(r'<link rel="canonical" href="([^"]+)"',text,re.I)
        if not m or not m.group(1).startswith(BASE): continue
        im=re.search(r'<img[^>]+src="(/assets/photos/[^"]+)"',text,re.I)
        rows[m.group(1)]=BASE+im.group(1) if im else None
    parts=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for url in sorted(rows):
        parts.append('<url><loc>'+xml_escape(url)+'</loc>')
        if rows[url]: parts.append('<image:image><image:loc>'+xml_escape(rows[url])+'</image:loc></image:image>')
        parts.append('</url>')
    parts.append('</urlset>'); (PUBLIC/'sitemap.xml').write_text(''.join(parts),encoding='utf-8')

def main():
    cases=load_cases(); build_pages(cases); patch_english_hreflang(); patch_local_homes(); rebuild_sitemap()
    pages=list(PUBLIC.glob('*/resources/guides/*/index.html'))
    assert len(pages)==20, len(pages)
    for slug in PRIORITY:
        en=(PUBLIC/'resources'/'guides'/slug/'index.html').read_text(encoding='utf-8')
        for code,l in LOCALES.items():
            assert f'hreflang="{l["lang"]}"' in en
            lp=(PUBLIC/code/'resources'/'guides'/slug/'index.html').read_text(encoding='utf-8')
            assert 'hreflang="en"' in lp and 'hreflang="x-default"' in lp and '"@type":"Article"' in lp
    print('Multilingual guide SEO OK: 20 localized detail pages + 5 hubs + reciprocal hreflang')

if __name__=='__main__': main()
