#!/usr/bin/env python3
import html, json, re
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'
BASE='https://pomerol.in'
ORG_ID=BASE+'/#organization'
TODAY=date.today().isoformat()

def esc(v): return html.escape(str(v),quote=True)
def slugify(v): return re.sub(r'[^a-z0-9]+','-',v.lower()).strip('-')

def solutions():
    out=[]
    for n in ('seo_pages_core.json','seo_pages_industries.json'):
        out += json.loads((ROOT/'scripts'/n).read_text(encoding='utf-8'))
    return out

def cases():
    out=[]
    for i in range(1,5):
        t=(PUBLIC/'assets'/f'cases-part-{i}.js').read_text(encoding='utf-8').strip()
        if i==1:
            raw=t.removeprefix('window.CASE_LIBRARY=').rstrip(';')
        else:
            raw=t.removeprefix('window.CASE_LIBRARY.push(...').rstrip(';')
            if raw.endswith(')'): raw=raw[:-1]
        out += json.loads(raw)
    return out

def append_schema(path,obj):
    text=path.read_text(encoding='utf-8')
    m=re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)
    if not m: raise RuntimeError(f'No JSON-LD in {path}')
    data=json.loads(m.group(1)); graph=data.setdefault('@graph',[])
    marker=obj.get('@id')
    if not any(x.get('@id')==marker for x in graph if isinstance(x,dict)):
        graph.append(obj)
    packed=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    text=text[:m.start(1)]+packed+text[m.end(1):]
    path.write_text(text,encoding='utf-8')

def add_specialized_schema(sol,case_rows):
    for s in sol:
        url=f"{BASE}/{s['slug']}/"
        append_schema(PUBLIC/s['slug']/'index.html',{
            '@type':'Service','@id':url+'#service','name':s['title'],
            'description':s['description'],'provider':{'@id':ORG_ID},
            'areaServed':'Worldwide','serviceType':s['title'],'url':url
        })
    for c in case_rows:
        slug=f"{c['n']}-{slugify(c['title'])}"; url=f'{BASE}/case-studies/{slug}/'
        desc=f'Representative {c["industry"].lower()} sourcing case for a {c["profile"].lower()} in {c["market"]}: supplier work, controls and outcome.'
        append_schema(PUBLIC/'case-studies'/slug/'index.html',{
            '@type':'Article','@id':url+'#article','headline':c['title'],
            'description':desc,'image':f'{BASE}/assets/photos/{c["photo"]}',
            'author':{'@id':ORG_ID},'publisher':{'@id':ORG_ID},
            'mainEntityOfPage':url,'datePublished':TODAY,'dateModified':TODAY,
            'articleSection':c['industry'],'keywords':c['tags'],'inLanguage':'en'
        })

def add_internal_links(sol):
    for rel in ('index.html','en/index.html'):
        p=PUBLIC/rel; text=p.read_text(encoding='utf-8')
        text=text.replace('<h3>Supplier sourcing & RFQ</h3>','<h3><a href="/china-sourcing-agent/">Supplier sourcing & RFQ</a></h3>')
        text=text.replace('<h3>OEM / ODM coordination</h3>','<h3><a href="/china-oem-odm-sourcing/">OEM / ODM coordination</a></h3>')
        text=text.replace('<h3>Qualification, QC & export</h3>','<h3><a href="/china-quality-inspection/">Qualification, QC & export</a></h3>')
        p.write_text(text,encoding='utf-8')
    p=PUBLIC/'services'/'index.html'; text=p.read_text(encoding='utf-8')
    if 'data-seo-service-directory' not in text:
        cards=''.join(f'<article class="card"><div class="eyebrow">Sourcing guide</div><h3><a href="/{esc(s["slug"])}/">{esc(s["title"])}</a></h3><p>{esc(s["description"])}</p></article>' for s in sol)
        block='<section class="section" data-seo-service-directory><div class="wrap"><div class="section-head"><div><div class="eyebrow">Sourcing guides</div><h2 class="display">China sourcing services by buyer intent and industry.</h2></div><p>Detailed service pages connect procurement questions with relevant sourcing cases and control methods.</p></div><div class="grid-3">'+cards+'</div></div></section>'
        text=text.replace('</main>',block+'</main>',1)
        p.write_text(text,encoding='utf-8')

def main():
    sol=solutions(); case_rows=cases()
    assert len(sol)==14 and len(case_rows)==36
    add_specialized_schema(sol,case_rows)
    add_internal_links(sol)
    service=(PUBLIC/'china-sourcing-agent'/'index.html').read_text(encoding='utf-8')
    article=next((PUBLIC/'case-studies').glob('*/index.html')).read_text(encoding='utf-8')
    assert '"@type":"Service"' in service
    assert '"@type":"Article"' in article
    assert 'data-seo-service-directory' in (PUBLIC/'services'/'index.html').read_text(encoding='utf-8')
    print('SEO enhancement OK: Service/Article schemas and internal link directory')

if __name__=='__main__': main()
