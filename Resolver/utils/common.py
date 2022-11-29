import ipaddress
import random
import requests
from urllib.parse import urlencode
from plugins.imdb import getMovieInfo
from classes.browser import Firefox
from classes.net import NET
import re

CIDRs = {}

CIDRs["us"] = [
    "68.121.80.248/30",
    "68.121.80.252/31",
    "68.121.80.255/32",

    "12.232.30.252/31",
    "12.232.30.255/32",
    "12.232.30.248/30",

    "47.189.48.255/32",
    "47.189.48.254/32",
    "47.189.48.248/30",

    "24.218.158.128/26",
    "24.218.158.128/26",
    "24.218.158.192/27",
]

CIDRs["sk"] = [
    "78.98.0.0/16",
    "78.99.0.0/17",
    "78.99.128.0/18",
    "78.99.192.0/19",

    "80.242.32.0/21",
    "80.242.40.0/22",
    "80.242.44.0/23",
    "80.242.46.0/24",

    "178.143.0.0/17",
    "178.143.128.0/18",
    "178.143.192.0/19",
    "178.143.224.0/20",

    "185.1.34.0/25",
    "185.1.34.128/26",
    "185.1.34.192/27",
    "185.1.34.224/28",
]

CIDRs["cz"] = [
    "103.119.108.0/25",
    "103.119.108.128/26",
    "103.119.108.192/27",
    "103.119.108.224/28",

    "109.235.0.0/22",
    "109.235.4.0/23",
    "109.235.6.0/24",
    "109.235.7.0/25",

    "130.193.8.0/21",
    "130.193.16.0/22",
    "130.193.20.0/23",
    "130.193.22.0/24",

    "152.89.75.128/26",
    "152.89.75.192/27",
    "152.89.75.224/28",
    "152.89.75.240/29",
]

def genIP(country):
    """
    Args:
        country (str): Abbr. of country to use, ex. US, CZ, case insensitive

    Returns:
        ip (str): Result ip is random
    """
    
    CIDR = random.choice(CIDRs[country.lower()])
    ips = [str(ip) for ip in ipaddress.IPv4Network(CIDR)]
    return random.choice(ips)


def girc(page_data, url, co, useNET=False):
    """
    Code adapted from https://github.com/vb6rocod/utils/
    Copyright (C) 2019 vb6rocod
    and https://github.com/addon-lab/addon-lab_resolver_Project
    Copyright (C) 2021 ADDON-LAB, KAR10S
    """
    if useNET:
        net = NET()
    else:
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

def translateItemToCzech(id, isMovie):
    url = "https://www.csfd.cz/api/search/autocomplete/?q=" + getMovieInfo(id)["title"]
    headers = {
        "User-Agent": Firefox().ua,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.csfd.cz/",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1"
    }

    resp = requests.get(url, headers=headers).json()
    if isMovie: return resp['films'][0]['name']
    return resp['series'][0]['name']