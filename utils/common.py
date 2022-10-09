import random
import requests
from string import ascii_lowercase, digits
from utils.settings import getSetting
from utils.fakeBrowser import UA
from urllib.parse import urlencode
import socket
import os
import re

symbols = "[@_!#$%^&*()<>?/\|}{~:]\"'"
exceptions = ["!", ":", "?"]

def girc(page_data, url, co):
    """
    Code adapted from https://github.com/vb6rocod/utils/
    Copyright (C) 2019 vb6rocod
    and https://github.com/addon-lab/addon-lab_resolver_Project
    Copyright (C) 2021 ADDON-LAB, KAR10S
    """
    net = requests.Session()
    hdrs = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
            'Referer': url}
    rurl = 'https://www.google.com/recaptcha/api.js'
    aurl = 'https://www.google.com/recaptcha/api2'
    key = re.search(r'(?:src="{0}\?.*?render|data-sitekey)="?([^"]+)'.format(rurl), page_data)
    if key:
        key = key.group(1)
        rurl = '{0}?render={1}'.format(rurl, key)
        page_data1 = net.get(rurl, headers=hdrs).text
        v = re.findall('releases/([^/]+)', page_data1)[0]
        rdata = {'ar': 1,
                 'k': key,
                 'co': co,
                 'hl': 'en',
                 'v': v,
                 'size': 'invisible',
                 'cb': '123456789'}
        page_data2 = net.get('{0}/anchor?{1}'.format(aurl, urlencode(rdata)), headers=hdrs).text
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
        page_data3 = net.post('{0}/reload?k={1}'.format(aurl, key), data=pdata, headers=hdrs).text
        gtoken = re.search('rresp","([^"]+)', page_data3)
        if gtoken:
            return gtoken.group(1)
    return ''

def randStr(length = 32):
    s = ''.join(random.choice(ascii_lowercase + digits) for _ in range(length))
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