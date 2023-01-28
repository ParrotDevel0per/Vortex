import random
import requests
from string import ascii_lowercase, digits, ascii_uppercase
from utils.settings import getSetting
from urllib.parse import urlencode
import socket
import os
import base64
import re
from classes.net import NET

symbols = "[@_!#$%^&*()<>?/\|}{~:]\"'"
exceptions = ["!", ":", "?"]

def baseurl(request):
    resp = request.url_root[:-1]
    if getSetting("forceHTTPS").lower() == "true":
        resp = resp.replace("http://", "https://")
    return resp
    return request.url_root.split(f"/{request.url_root.split('/')[-2]}")[0]

def insertInMiddle(string, item):
    midPoint = len(string)//2
    return string[:midPoint] + item + string[midPoint:]

def girc(page_data, url, co, key="", useProxy=False, usePHPProxy=False):
    """
    Code adapted from https://github.com/vb6rocod/utils/
    Copyright (C) 2019 vb6rocod
    and https://github.com/addon-lab/addon-lab_resolver_Project
    Copyright (C) 2021 ADDON-LAB, KAR10S
    """
    net = NET()
    hdrs = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
            'Referer': url}
    rurl = 'https://www.google.com/recaptcha/api.js'
    aurl = 'https://www.google.com/recaptcha/api2'
    if not key:
        key = re.search(r'(?:src="{0}\?.*?render|data-sitekey)="?([^"]+)'.format(rurl), page_data)
    if key:
        if type(key) != str:
            key = key.group(1)
        rurl = '{0}?render={1}'.format(rurl, key)
        page_data1 = net.get(rurl, headers=hdrs, useProxy=useProxy, usePHPProxy=usePHPProxy).text
        v = re.findall('releases/([^/]+)', page_data1)[0]
        rdata = {'ar': 1,
                 'k': key,
                 'co': co,
                 'hl': 'en',
                 'v': v,
                 'size': 'invisible',
                 'cb': '123456789'}
        page_data2 = net.get('{0}/anchor?{1}'.format(aurl, urlencode(rdata)), headers=hdrs, useProxy=useProxy, usePHPProxy=usePHPProxy).text
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
        page_data3 = net.post('{0}/reload?k={1}'.format(aurl, key), data=pdata, headers=hdrs, useProxy=useProxy, usePHPProxy=usePHPProxy).text
        gtoken = re.search('rresp","([^"]+)', page_data3)
        if gtoken:
            return gtoken.group(1)

    return ''

def randStr(length = 32, incUpper=False):
    f = ascii_lowercase + digits
    if incUpper: f += ascii_uppercase
    s = ''.join(random.choice(f) for _ in range(length))
    return s

def chunkedDownload(url, filename, chunkSize=8192):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunkSize):
            if chunk:
                f.write(chunk)
    return filename

def sanitize(text):
    for symbol in symbols:
        if symbol not in exceptions:
            text = text.replace(symbol, "")
    return text

def getLocalIP():
    ip = getSetting('ip')
    hostname = socket.gethostname()
    if ip == "0.0.0.0":return socket.gethostbyname(hostname)
    return ip

def cls():
    if os.name == "nt": os.system("cls")
    else: os.system("clear")

# https://stackoverflow.com/questions/34327719/get-keys-from-json-in-python
def get_simple_keys(data):
    result = []
    for key in data.keys():
        if type(data[key]) != dict:
            result.append(key)
        else:
            result += get_simple_keys(data[key])
    return result


def base64encode(data):
    return base64.b64encode(data.encode()).decode()

def base64decode(data):
    return base64.b64decode(data.encode()).decode()

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
