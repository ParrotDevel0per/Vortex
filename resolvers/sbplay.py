import re
import base64
import binascii
import random
import string
import requests
import json
from utils.fakeBrowser import UA
from urllib.parse import urlparse, urlencode

def girc(page_data, url, co):
    """
    Code adapted from https://github.com/vb6rocod/utils/
    Copyright (C) 2019 vb6rocod
    and https://github.com/addon-lab/addon-lab_resolver_Project
    Copyright (C) 2021 ADDON-LAB, KAR10S
    """
    net = requests.session()
    hdrs = {'User-Agent': UA,
            'Referer': url}
    rurl = 'https://www.google.com/recaptcha/api.js'
    aurl = 'https://www.google.com/recaptcha/api2'
    key = re.search(r'(?:src="{0}\?.*?render|data-sitekey)="?([^"]+)'.format(rurl), page_data)
    if key:
        key = key.group(1)
        rurl = '{0}?render={1}'.format(rurl, key)
        page_data1 = net.http_GET(rurl, headers=hdrs).content
        v = re.findall('releases/([^/]+)', page_data1)[0]
        rdata = {'ar': 1,
                 'k': key,
                 'co': co,
                 'hl': 'en',
                 'v': v,
                 'size': 'invisible',
                 'cb': '123456789'}
        page_data2 = net.http_GET('{0}/anchor?{1}'.format(aurl, urlencode(rdata)), headers=hdrs).content
        rtoken = re.search('recaptcha-token.+?="([^"]+)', page_data2)
        if rtoken:
            rtoken = rtoken.group(1)
        else:
            return ''
        pdata = {'v': v,
                 'reason': 'q',
                 'k': key,
                 'c': rtoken,
                 'sa': '',
                 'co': co}
        hdrs.update({'Referer': aurl})
        page_data3 = net.http_POST('{0}/reload?k={1}'.format(aurl, key), form_data=pdata, headers=hdrs).content
        gtoken = re.search('rresp","([^"]+)', page_data3)
        if gtoken:
            return gtoken.group(1)

def cleanse_html(html):
    for match in re.finditer('<!--(.*?)-->', html, re.DOTALL):
        if match.group(1)[-2:] != '//':
            html = html.replace(match.group(0), '')

    html = re.sub(r'''<(div|span)[^>]+style=["'](visibility:\s*hidden|display:\s*none);?["']>.*?</\\1>''', '', html, re.I | re.DOTALL)
    return html

def get_hidden(html, form_id=None, index=None, include_submit=True):
    hidden = {}
    if form_id:
        pattern = r'''<form [^>]*(?:id|name)\s*=\s*['"]?%s['"]?[^>]*>(.*?)</form>''' % (form_id)
    else:
        pattern = '''<form[^>]*>(.*?)</form>'''

    html = cleanse_html(html)

    for i, form in enumerate(re.finditer(pattern, html, re.DOTALL | re.I)):
        if index is None or i == index:
            for field in re.finditer('''<input [^>]*type=['"]?hidden['"]?[^>]*>''', form.group(1)):
                match = re.search(r'''name\s*=\s*['"]([^'"]+)''', field.group(0))
                match1 = re.search(r'''value\s*=\s*['"]([^'"]*)''', field.group(0))
                if match and match1:
                    hidden[match.group(1)] = match1.group(1)

            if include_submit:
                match = re.search('''<input [^>]*type=['"]?submit['"]?[^>]*>''', form.group(1))
                if match:
                    name = re.search(r'''name\s*=\s*['"]([^'"]+)''', match.group(0))
                    value = re.search(r'''value\s*=\s*['"]([^'"]*)''', match.group(0))
                    if name and value:
                        hidden[name.group(1)] = value.group(1)

    return hidden

def sbplay(web_url):
    parsed = urlparse(web_url)
    host = parsed.netloc
    media_id = parsed.path.replace("/e/", "").replace("/d/", "")

    rurl = 'https://{0}/'.format(host)
    headers = {'User-Agent': UA,
               'Referer': rurl}
    html = requests.get(web_url, headers=headers).text
    sources = re.findall(r'download_video([^"]+)[^\d]+\d+x(\d+)', html)
    if sources:
        sources.sort(key=lambda x: int(x[1]), reverse=True)
        sources = [(x[1] + 'p', x[0]) for x in sources]
        print(sources)
        code, mode, dl_hash = sources
        dl_url = 'https://{0}/dl?op=download_orig&id={1}&mode={2}&hash={3}'.format(host, code, mode, dl_hash)
        html = requests.get(dl_url, headers=headers).text
        domain = base64.b64encode((rurl[:-1] + ':443').encode('utf-8')).decode('utf-8').replace('=', '')
        token = girc(html, rurl, domain)
        if token:
            payload = get_hidden(html)
            payload.update({'g-recaptcha-response': token})
            req = requests.post(dl_url, form_data=payload, headers=headers).text
            r = re.search('href="([^"]+).+?>(?:Direct|Download)', req)
            if r:
                return r.group(1), headers

    eurl = get_embedurl(host, media_id)
    headers.update({'watchsb': 'sbstream'})
    html = requests.get(eurl, headers=headers).text
    data = json.loads(html).get("stream_data", {})
    strurl = data.get('file') or data.get('backup')
    if strurl:
        headers.pop('watchsb')
        return strurl, headers

    

def get_embedurl(host, media_id):
    # Copyright (c) 2019 vb6rocod
    def makeid(length):
        t = string.ascii_letters + string.digits
        return ''.join([random.choice(t) for _ in range(length)])

    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), media_id, makeid(12))
    c1 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), makeid(12), makeid(12))
    c2 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    x = '{0}||{1}||{2}||streamsb'.format(makeid(12), c2, makeid(12))
    c3 = binascii.hexlify(x.encode('utf8')).decode('utf8')
    return 'https://{0}/sources48/{1}/{2}'.format(host, c1, c3)
