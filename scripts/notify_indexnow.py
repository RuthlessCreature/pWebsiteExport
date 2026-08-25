#!/usr/bin/env python3
from __future__ import annotations
import json,time,urllib.error,urllib.parse,urllib.request,xml.etree.ElementTree as ET

HOST='pomerol.in'
BASE='https://pomerol.in'
KEY='6ef27e4a81efe1ff6c679ee852d012f2'
KEY_URL=f'{BASE}/{KEY}.txt'
ENDPOINTS=['https://api.indexnow.org/indexnow','https://www.bing.com/indexnow']
UA='PomerolInternational-IndexNow/2.0 (+https://pomerol.in/)'


def fetch_text(url):
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Cache-Control':'no-cache','Accept':'text/plain,*/*;q=0.8'})
    with urllib.request.urlopen(req,timeout=20) as r:
        return r.status,r.geturl(),dict(r.headers.items()),r.read().decode('utf-8','replace').strip()


def wait_for_key():
    last=None
    for attempt in range(1,7):
        try:
            status,final_url,headers,body=fetch_text(KEY_URL+f'?v={int(time.time())}')
            if status==200 and final_url.startswith(KEY_URL) and body==KEY:
                print(f'IndexNow key verified on attempt {attempt}: status={status} final={final_url} content-type={headers.get("Content-Type","")}')
                return True
            last=f'status={status} final={final_url} body={body[:100]!r}'
        except Exception as e:
            last=repr(e)
        time.sleep(min(attempt*2,10))
    print('IndexNow key verification failed:',last)
    return False


def sitemap_urls():
    root=ET.parse('public/sitemap.xml').getroot()
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[n.text.strip() for n in root.findall('s:url/s:loc',ns) if n.text and n.text.strip().startswith(BASE+'/')]
    return list(dict.fromkeys(urls))


def http_error_body(e):
    try:
        return e.read().decode('utf-8','replace').strip()[:500]
    except Exception:
        return ''


def bulk_submit(endpoint,urls):
    payload=json.dumps({'host':HOST,'key':KEY,'keyLocation':KEY_URL,'urlList':urls},separators=(',',':')).encode('utf-8')
    req=urllib.request.Request(endpoint,data=payload,headers={
        'Content-Type':'application/json; charset=utf-8',
        'Accept':'application/json,text/plain,*/*',
        'User-Agent':UA,
    },method='POST')
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            body=r.read().decode('utf-8','replace').strip()[:500]
            print('IndexNow bulk endpoint:',endpoint,'status:',r.status,'URLs:',len(urls),'body:',repr(body))
            return 200 <= r.status < 300
    except urllib.error.HTTPError as e:
        print('IndexNow bulk endpoint:',endpoint,'HTTP:',e.code,'reason:',e.reason,'body:',repr(http_error_body(e)))
        return False
    except Exception as e:
        print('IndexNow bulk endpoint:',endpoint,'error:',repr(e))
        return False


def single_submit(endpoint,url):
    q=urllib.parse.urlencode({'url':url,'key':KEY,'keyLocation':KEY_URL})
    req=urllib.request.Request(endpoint+'?'+q,headers={'User-Agent':UA,'Accept':'text/plain,*/*'})
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            body=r.read().decode('utf-8','replace').strip()[:500]
            print('IndexNow single endpoint:',endpoint,'status:',r.status,'URL:',url,'body:',repr(body))
            return 200 <= r.status < 300
    except urllib.error.HTTPError as e:
        print('IndexNow single endpoint:',endpoint,'HTTP:',e.code,'reason:',e.reason,'URL:',url,'body:',repr(http_error_body(e)))
        return False
    except Exception as e:
        print('IndexNow single endpoint:',endpoint,'error:',repr(e))
        return False


def main():
    if not wait_for_key():
        raise SystemExit(2)
    urls=sitemap_urls()
    if not urls:
        raise SystemExit('No sitemap URLs')
    print('IndexNow diagnostic context: host=',HOST,'keyLocation=',KEY_URL,'sitemapURLs=',len(urls))
    priority=next((u for u in urls if u.endswith('/en/')),urls[0])
    single_ok=False
    for endpoint in ENDPOINTS:
        if single_submit(endpoint,priority):
            single_ok=True
            break
    if not single_ok:
        raise SystemExit(3)
    chunk_size=100
    for start in range(0,len(urls),chunk_size):
        chunk=urls[start:start+chunk_size]
        accepted=False
        for endpoint in ENDPOINTS:
            if bulk_submit(endpoint,chunk):
                accepted=True
                break
        if not accepted:
            raise SystemExit(4)
    print('IndexNow submission accepted for',len(urls),'URLs')


if __name__=='__main__':
    main()
