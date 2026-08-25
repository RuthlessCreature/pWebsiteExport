#!/usr/bin/env python3
from __future__ import annotations
import json,time,urllib.error,urllib.parse,urllib.request,xml.etree.ElementTree as ET

HOST='pomerol.in'
BASE='https://pomerol.in'
KEY='02289c9f560410ae6b1db5dab06ccccc'
KEY_URL=f'{BASE}/{KEY}.txt'
BULK_ENDPOINTS=['https://api.indexnow.org/indexnow','https://www.bing.com/indexnow']
SINGLE_ENDPOINTS=['https://api.indexnow.org/indexnow','https://www.bing.com/indexnow']

def fetch_text(url):
    req=urllib.request.Request(url,headers={'User-Agent':'PomerolSEO/1.0','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=20) as r:
        return r.status,r.read().decode('utf-8','replace').strip()

def wait_for_key():
    last=None
    for attempt in range(1,7):
        try:
            status,body=fetch_text(KEY_URL+f'?v={int(time.time())}')
            if status==200 and body==KEY:
                print(f'IndexNow key verified on attempt {attempt}')
                return True
            last=f'status={status} body={body[:80]!r}'
        except Exception as e:
            last=repr(e)
        time.sleep(min(attempt*2,10))
    print('IndexNow key verification failed:',last)
    return False

def sitemap_urls():
    root=ET.parse('public/sitemap.xml').getroot()
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    return [n.text for n in root.findall('s:url/s:loc',ns) if n.text and n.text.startswith(BASE+'/')]

def bulk_submit(endpoint,urls):
    # Root-key protocol (IndexNow Option 1): keyLocation is intentionally omitted.
    payload=json.dumps({'host':HOST,'key':KEY,'urlList':urls}).encode()
    req=urllib.request.Request(endpoint,data=payload,headers={'Content-Type':'application/json; charset=utf-8','User-Agent':'PomerolSEO/1.0'})
    try:
        with urllib.request.urlopen(req,timeout=25) as r:
            print('IndexNow bulk endpoint:',endpoint,'status:',r.status,'URLs:',len(urls))
            return 200 <= r.status < 300
    except urllib.error.HTTPError as e:
        print('IndexNow bulk endpoint:',endpoint,'HTTP:',e.code)
        return False
    except Exception as e:
        print('IndexNow bulk endpoint:',endpoint,'error:',repr(e))
        return False

def single_submit(endpoint,url):
    q=urllib.parse.urlencode({'url':url,'key':KEY})
    req=urllib.request.Request(endpoint+'?'+q,headers={'User-Agent':'PomerolSEO/1.0'})
    try:
        with urllib.request.urlopen(req,timeout=25) as r:
            print('IndexNow single endpoint:',endpoint,'status:',r.status,'URL:',url)
            return 200 <= r.status < 300
    except urllib.error.HTTPError as e:
        print('IndexNow single endpoint:',endpoint,'HTTP:',e.code,'URL:',url)
        return False
    except Exception as e:
        print('IndexNow single endpoint:',endpoint,'error:',repr(e))
        return False

def main():
    if not wait_for_key(): raise SystemExit(2)
    urls=sitemap_urls()
    if not urls: raise SystemExit('No sitemap URLs')
    for endpoint in BULK_ENDPOINTS:
        if bulk_submit(endpoint,urls): return
    # Diagnostic fallback using the simplest protocol form on the highest-value URL.
    priority=next((u for u in urls if u.endswith('/en/')),urls[0])
    for endpoint in SINGLE_ENDPOINTS:
        if single_submit(endpoint,priority):
            print('Bulk submission rejected, but root-key single URL submission works.')
            return
    raise SystemExit(3)

if __name__=='__main__': main()
