from utils.unpacker import unpack
from utils.fakeBrowser import baseHeaders
import requests
import re

def grab(self, url, referer=None, mxr=True):
    headers = baseHeaders
    headers.update({'Referer': 'https://mixdrop.co/'})
    if referer: headers.update({'Referer': referer})
    html = requests.get(url, headers=headers).text
    if not "(p,a,c,k,e,d)" in html: return None
    packed = "eval" + html.split("eval")[1].split(".split('|'),0,{}))")[0] + ".split('|'),0,{}))"
    unpacked = unpack(packed)
    pattern = r"wurl=\"(.*?)\""
    match = re.search(pattern, unpacked)
    if mxr: headers.update({"Referer": "https://mixdrop.co/"})
    if match: return "https:" + match.group(1), headers
    return None, None